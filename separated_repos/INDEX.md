# StrepSuis Suite - Separated Modules Documentation

**Repository**: MK-vet/MKrep  
**Last Updated**: 2025-11-26  
**Status**: Production-Ready

## 📋 Quick Navigation

| Document | Purpose | Target Audience |
|----------|---------|-----------------|
| **[INDEX.md](INDEX.md)** | Main documentation index | All users |
| **[COVERAGE_RESULTS.md](COVERAGE_RESULTS.md)** | Test coverage analysis | Developers |
| **[END_TO_END_TESTS.md](END_TO_END_TESTS.md)** | E2E test documentation | Developers, QA |
| **[ANALYSIS_EXAMPLES.md](ANALYSIS_EXAMPLES.md)** | Complete analysis examples | Researchers, users |
| **[README.md](README.md)** | Modules overview | All users |
| **[IMPLEMENTATION_COMPLETE_COVERAGE.md](IMPLEMENTATION_COMPLETE_COVERAGE.md)** | Implementation summary | Developers, reviewers |

## 📊 Module Overview

### Core Modules (Production-Ready)

| Module | Coverage | Status | Primary Function |
|--------|----------|--------|------------------|
| [strepsuis-amrpat](strepsuis-amrpat/) | **62%** ✅ | Production | MDR pattern detection |
| [strepsuis-amrvirkm](strepsuis-amrvirkm/) | **34%** ⚠️ | Needs improvement | K-modes clustering |
| [strepsuis-genphen](strepsuis-genphen/) | **32%** ⚠️ | Needs improvement | Genotype-phenotype integration |
| [strepsuis-genphennet](strepsuis-genphennet/) | **36%** ⚠️ | Needs improvement | Network-based analysis |
| [strepsuis-phylotrait](strepsuis-phylotrait/) | **22%** ❌ | Critical improvement | Phylogenetic + traits |

**Overall Quality**:
- ✅ All modules have **80-100% coverage** of critical infrastructure (config, CLI, orchestration)
- ✅ All modules have comprehensive **end-to-end tests** validating complete workflows
- ⚠️ Analysis algorithm coverage varies (validated through integration tests)
- 🎯 Target: All modules at **60%+ coverage** by Q1 2026

## 🚀 Quick Start

See [ANALYSIS_EXAMPLES.md](ANALYSIS_EXAMPLES.md) for comprehensive examples with real data.

---

**Version**: 1.0.0  
**Status**: Production-Ready (with improvement roadmap)
