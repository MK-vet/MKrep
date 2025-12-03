# Release Checklist for StrepSuis Analyzer

## Pre-Release

### Code Quality
- [ ] All tests pass locally
- [ ] Code coverage meets minimum threshold (35%+)
- [ ] No critical linting errors
- [ ] Type hints are consistent
- [ ] Security scan (Bandit) passes
- [ ] CodeQL analysis passes

### Documentation
- [ ] README.md is up to date
- [ ] CHANGELOG.md includes all changes
- [ ] USER_GUIDE.md reflects current functionality
- [ ] TESTING.md is accurate
- [ ] API documentation is current
- [ ] Example notebooks work correctly

### Testing
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All workflow tests pass
- [ ] Statistical validation tests pass
- [ ] CLI tests pass
- [ ] Docker build succeeds
- [ ] Docker container runs correctly
- [ ] Notebook execution succeeds

### Dependencies
- [ ] requirements.txt is up to date
- [ ] pyproject.toml dependencies are correct
- [ ] No known security vulnerabilities
- [ ] License compliance checked

### Examples
- [ ] Example data is current
- [ ] Example outputs are regenerated
- [ ] Notebooks produce expected results
- [ ] Docker compose example works

## Version Bump

- [ ] Update version in `pyproject.toml`
- [ ] Update version in `strepsuis_analyzer/__init__.py`
- [ ] Update version in Dockerfile labels
- [ ] Update version in CITATION.cff
- [ ] Update version in README.md badges (if applicable)

## Git Operations

- [ ] All changes committed
- [ ] Branch is up to date with main
- [ ] No merge conflicts
- [ ] Clean git status

## Create Release

### GitHub Release
- [ ] Create git tag: `git tag -a v2025.8.11 -m "Release v2025.8.11"`
- [ ] Push tag: `git push origin v2025.8.11`
- [ ] Create GitHub release from tag
- [ ] Add release notes from CHANGELOG.md
- [ ] Upload built packages (if applicable)

### Release Notes
- [ ] Summary of changes
- [ ] Breaking changes highlighted
- [ ] New features listed
- [ ] Bug fixes listed
- [ ] Known issues documented
- [ ] Installation instructions
- [ ] Migration guide (if needed)

## Post-Release

### Verification
- [ ] GitHub Actions CI passes
- [ ] Docker image builds successfully
- [ ] Docker image is pushed to registry
- [ ] PyPI package is uploaded (if applicable)
- [ ] Documentation is published
- [ ] Release announcement is prepared

### Communication
- [ ] Update repository README if needed
- [ ] Announce on project communication channels
- [ ] Update documentation website (if applicable)
- [ ] Close related issues
- [ ] Thank contributors

### Monitoring
- [ ] Monitor for bug reports
- [ ] Check download metrics
- [ ] Review user feedback
- [ ] Plan next release cycle

## Rollback Plan

If issues are discovered post-release:

1. **Minor Issue**
   - Create hotfix branch
   - Fix issue
   - Release patch version

2. **Major Issue**
   - Document the issue
   - Create GitHub issue
   - Consider yanking release
   - Prepare hotfix release

## Version Numbering

We use calendar versioning: `YYYY.M.MICRO`

- `YYYY`: Year (e.g., 2025)
- `M`: Month (e.g., 8 for August)
- `MICRO`: Patch number (e.g., 11)

Examples:
- `2025.8.11` - August 11, 2025
- `2025.8.12` - Patch release
- `2025.9.1` - September 2025 release

## Emergency Hotfix Process

For critical security or bug fixes:

1. Create hotfix branch from release tag
2. Apply minimal fix
3. Test thoroughly
4. Update version (increment MICRO)
5. Follow abbreviated release checklist
6. Deploy immediately
7. Backfill full documentation

---

**Template Version**: 1.0  
**Last Updated**: 2025-08-11
