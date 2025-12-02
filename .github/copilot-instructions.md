Copilot instructions for working in MK-vet/MKrep/separated_repos
Use the following as persistent instructions whenever you work in this repository.

### 1. Repository Structure & Context
This directory contains four distinct sub-projects. Treat them as individual packages sharing a common rigorous standard:
- `strepsuis-mdr` (Likely the reference implementation; check this first for patterns)
- `strepsuis-amrvirkm`
- `strepsuis-genphennet`
- `strepsuis-phylotrait`

**Global Standards:**
- Consult `MATHEMATICAL_VALIDATION.md` and `SYNTHETIC_DATA_VALIDATION.md` before modifying any numerical logic.
- Usage of `replicate_tests.py` and `run_tests.sh` is standard for verification.
- `COVERAGE_RESULTS.md` tracks the current test status; updates must be reflected there.

### 2. Development Guidelines
**Preserve Production Behavior:**
- Consider all code in `strepsuis-*/` packages as production-grade.
- Do not break downstream dependencies: CLIs, Dockerfiles, and Notebooks (under `notebooks/` in each sub-repo) rely on the current API.
- If a change is required, prioritize backwards compatibility or explicitly update all 3 execution contexts:
    1. **Library** (Python package)
    2. **CLI** (Command line entry points)
    3. **Docker** (Dockerfile & docker-compose.yml)

**Refactoring & Cleanup:**
- **Do not rewrite from scratch.** Assume existing modules have been refactored for a reason.
- Focus on increasing test coverage and mathematical correctness.
- Merge over-fragmented files only if they result in a coherent logical unit.
- Remove dead code only after verifying it is not used in `notebooks/` or external scripts.

### 3. Testing & Coverage Targets
For each sub-repository (e.g., `strepsuis-mdr`):
- **Goal:** 100% coverage for core algorithms.
- **Tools:** Use `pytest` with the configuration in `pytest.ini`.
- **Process:**
    1. Convert any ad-hoc scripts (e.g., `test_functionality.py`) into formal `pytest` suites in `tests/`.
    2. Ensure tests run successfully via `run_tests.sh`.
    3. If coverage improves, run `generate_coverage_badge.py` and `add_coverage_badges.py` to update badges and reports.
- **Smoke Tests:** Every Docker image and CLI command must have at least one end-to-end "smoke test" verifying basic execution.

### 4. Mathematical & Statistical Validation
When touching code involved in clustering, network metrics, AMR analysis, or phylogenetics:
- **Mandatory:** Validate against `MATHEMATICAL_VALIDATION.md` guidelines.
- Create synthetic datasets (small, known ground-truth) to verify logic.
- Compare results against `scikit-learn`, `scipy`, or `numpy` baselines where applicable.
- Add tests for invariants (e.g., symmetry of distance matrices, probability sums = 1.0).

### 5. Documentation & Outputs
**Do not silently change outputs.**
- Existing CSVs, HTML reports, and Plots in `examples/` or `results/` are sources of truth.
- If a bug fix changes an output:
    1. Recompute the example output.
    2. Update the corresponding documentation (e.g., `ANALYSIS_EXAMPLES.md`).
    3. Explain the deviation in the PR/Commit message.

**User Guides:**
- Keep `USER_GUIDE.md` and `DEPLOYMENT_GUIDE.md` in sync with code changes.
- Ensure `WORKFLOW_USAGE_GUIDE.md` accurately reflects the CLI arguments.

### 6. Code Style
- **Python 3.11+**: Use strict type hints (`mypy` compatible).
- **Determinism**: All stochastic functions MUST accept a `random_state` or seed.
- **Safety**: No `eval()`, `exec()`, or unvalidated path handling.
- **Libraries**: Rely on `pyproject.toml` dependencies; do not add new heavy dependencies without justification.
