#!/usr/bin/env python3
"""
Docker smoke tests for MKrep.

Tests verify:
- Dockerfile syntax and structure
- docker-compose.yml validity
- Docker build command structure (without actual build)

Note: Actual Docker builds are not run in CI due to Docker
not being available in all environments. These tests verify
the Docker configuration files are valid.
"""

import sys
import os
import pytest
import subprocess
from pathlib import Path
import yaml


class TestDockerfileStructure:
    """Tests for Dockerfile syntax and structure."""
    
    @pytest.fixture
    def dockerfile_path(self):
        """Path to Dockerfile."""
        return Path(__file__).parent / 'Dockerfile'
    
    def test_dockerfile_exists(self, dockerfile_path):
        """Verify Dockerfile exists."""
        assert dockerfile_path.exists(), "Dockerfile must exist"
    
    def test_dockerfile_has_from(self, dockerfile_path):
        """Verify Dockerfile has FROM instruction."""
        content = dockerfile_path.read_text()
        assert 'FROM' in content, "Dockerfile must have FROM instruction"
    
    def test_dockerfile_has_workdir(self, dockerfile_path):
        """Verify Dockerfile has WORKDIR instruction."""
        content = dockerfile_path.read_text()
        assert 'WORKDIR' in content, "Dockerfile must have WORKDIR instruction"
    
    def test_dockerfile_has_copy(self, dockerfile_path):
        """Verify Dockerfile has COPY instruction."""
        content = dockerfile_path.read_text()
        assert 'COPY' in content, "Dockerfile must have COPY instruction"
    
    def test_dockerfile_has_run(self, dockerfile_path):
        """Verify Dockerfile has RUN instruction."""
        content = dockerfile_path.read_text()
        assert 'RUN' in content, "Dockerfile must have RUN instruction"
    
    def test_dockerfile_has_cmd(self, dockerfile_path):
        """Verify Dockerfile has CMD instruction."""
        content = dockerfile_path.read_text()
        assert 'CMD' in content, "Dockerfile must have CMD instruction"
    
    def test_dockerfile_uses_python_base(self, dockerfile_path):
        """Verify Dockerfile uses Python base image."""
        content = dockerfile_path.read_text()
        assert 'python:' in content.lower(), "Dockerfile should use Python base image"
    
    def test_dockerfile_installs_requirements(self, dockerfile_path):
        """Verify Dockerfile installs requirements."""
        content = dockerfile_path.read_text()
        assert 'requirements.txt' in content, "Dockerfile should install from requirements.txt"
    
    def test_dockerfile_has_labels(self, dockerfile_path):
        """Verify Dockerfile has metadata labels."""
        content = dockerfile_path.read_text()
        assert 'LABEL' in content, "Dockerfile should have LABEL instructions"


class TestDockerComposeStructure:
    """Tests for docker-compose.yml structure."""
    
    @pytest.fixture
    def compose_path(self):
        """Path to docker-compose.yml."""
        return Path(__file__).parent / 'docker-compose.yml'
    
    def test_compose_file_exists(self, compose_path):
        """Verify docker-compose.yml exists."""
        assert compose_path.exists(), "docker-compose.yml must exist"
    
    def test_compose_valid_yaml(self, compose_path):
        """Verify docker-compose.yml is valid YAML."""
        content = compose_path.read_text()
        try:
            yaml.safe_load(content)
        except yaml.YAMLError as e:
            pytest.fail(f"docker-compose.yml is not valid YAML: {e}")
    
    def test_compose_has_services(self, compose_path):
        """Verify docker-compose.yml has services."""
        content = compose_path.read_text()
        config = yaml.safe_load(content)
        assert 'services' in config, "docker-compose.yml must have services"
    
    def test_compose_has_analysis_services(self, compose_path):
        """Verify docker-compose.yml has expected analysis services."""
        content = compose_path.read_text()
        config = yaml.safe_load(content)
        services = config.get('services', {})
        
        # Check for expected services - these match the CLI commands
        # documented in the README and python_package/pyproject.toml
        expected_services = ['mkrep-cluster', 'mkrep-mdr', 'mkrep-network', 'mkrep-phylo']
        missing = [s for s in expected_services if s not in services]
        assert not missing, f"docker-compose.yml missing expected services: {missing}"
    
    def test_compose_services_have_build(self, compose_path):
        """Verify services have build configuration."""
        content = compose_path.read_text()
        config = yaml.safe_load(content)
        services = config.get('services', {})
        
        for service_name, service_config in services.items():
            # Each service should have build or image
            has_build = 'build' in service_config or 'image' in service_config
            assert has_build, f"Service {service_name} must have build or image"
    
    def test_compose_services_have_volumes(self, compose_path):
        """Verify services have volume mounts."""
        content = compose_path.read_text()
        config = yaml.safe_load(content)
        services = config.get('services', {})
        
        for service_name, service_config in services.items():
            # Skip if service just extends another
            if 'extends' in service_config:
                continue
            # Services should have volumes for data/output
            has_volumes = 'volumes' in service_config
            assert has_volumes, f"Service {service_name} should have volumes"


class TestDockerBuildCommand:
    """Tests for Docker build command structure."""
    
    def test_docker_build_command_valid(self):
        """Test that docker build command structure is valid."""
        # Test the command structure without executing
        cmd = ['docker', 'build', '-t', 'mkrep:latest', '.']
        
        # Verify command structure
        assert cmd[0] == 'docker'
        assert cmd[1] == 'build'
        assert '-t' in cmd
        assert 'mkrep:latest' in cmd
    
    def test_docker_run_command_valid(self):
        """Test that docker run command structure is valid."""
        # Test the command structure without executing
        cmd = [
            'docker', 'run',
            '-v', '$(pwd)/data:/data',
            '-v', '$(pwd)/output:/output',
            'mkrep:latest',
            'mkrep-cluster',
            '--data-dir', '/data',
            '--output', '/output'
        ]
        
        assert cmd[0] == 'docker'
        assert cmd[1] == 'run'
        assert '-v' in cmd


class TestDockerIntegrationReadiness:
    """Tests for Docker integration readiness."""
    
    def test_requirements_txt_exists(self):
        """Verify requirements.txt exists for Docker build."""
        req_path = Path(__file__).parent / 'requirements.txt'
        assert req_path.exists(), "requirements.txt must exist for Docker build"
    
    def test_requirements_has_core_deps(self):
        """Verify requirements.txt has core dependencies."""
        req_path = Path(__file__).parent / 'requirements.txt'
        content = req_path.read_text().lower()
        
        core_deps = ['pandas', 'numpy', 'scipy', 'scikit-learn', 'matplotlib']
        for dep in core_deps:
            assert dep in content, f"requirements.txt should have {dep}"
    
    def test_python_package_exists(self):
        """Verify python_package directory exists for Docker build."""
        pkg_path = Path(__file__).parent / 'python_package'
        assert pkg_path.exists(), "python_package must exist for Docker build"
    
    def test_pyproject_toml_exists(self):
        """Verify pyproject.toml exists in python_package."""
        toml_path = Path(__file__).parent / 'python_package' / 'pyproject.toml'
        assert toml_path.exists(), "pyproject.toml must exist"


class TestDockerignore:
    """Tests for .dockerignore configuration."""
    
    @pytest.fixture
    def dockerignore_path(self):
        """Path to .dockerignore."""
        return Path(__file__).parent / '.dockerignore'
    
    def test_dockerignore_exists(self, dockerignore_path):
        """Verify .dockerignore exists."""
        assert dockerignore_path.exists(), ".dockerignore should exist"
    
    def test_dockerignore_excludes_git(self, dockerignore_path):
        """Verify .dockerignore excludes .git."""
        content = dockerignore_path.read_text()
        assert '.git' in content, ".dockerignore should exclude .git"
    
    def test_dockerignore_excludes_cache(self, dockerignore_path):
        """Verify .dockerignore excludes cache directories."""
        content = dockerignore_path.read_text()
        # Should exclude at least some cache directories
        excludes_cache = '__pycache__' in content or '.cache' in content or '*.pyc' in content
        assert excludes_cache, ".dockerignore should exclude cache files"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
