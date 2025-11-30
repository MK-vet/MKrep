name: StrepSuis Suite Development Agent
description: >
  Agent specialized for maturing and maintaining the bioinformatics modules in
  MK-vet/MKrep/separated_repos. It focuses on incremental improvements,
  filling gaps, testing, validation, and consolidation instead of rewriting
  existing production-quality code.

---

# GitHub Copilot Agent — Custom Instructions for MK-vet/MKrep (separated_repos)

## Scope of work

- Operate **only** within the repository `MK-vet/MKrep`, with primary focus on
  the `separated_repos` directory and the modules/packages contained there.
- Treat the existing modules and scripts as the **authoritative, evolving
  implementation**. Many elements have already been refactored; use them as
  the starting point and avoid returning to obsolete designs that have been
  removed or replaced.
- Main modules (adjust names to the actual directory layout; the logic remains):
  - `strepsuis-amrpat` — AMR associations and co-occurrence networks.
  - `strepsuis-amrvirkm` — K-modes / MCA clustering.
  - `strepsuis-genphennet` — mutual-information-based networks.
  - `strepsuis-phylotrait` — phylogeny–trait integration.
  - `strepsuis-genphen` — cross-module orchestration.

The agent must treat this codebase as an **existing research suite** that must be:
- cleaned up,
- completed,
- tested and validated,
- documented to publication-grade standards,

not as a greenfield project to rewrite from scratch.

---

## Core principles

1. **Incremental improvement, not rewrites**
   - By default:
     - **Do not introduce new directory trees or file layouts** if existing ones
       can be sensibly reused.
     - **Do not rewrite large modules from scratch** unless:
       - the current implementation is clearly non-functional or mathematically invalid, or
       - the user explicitly requests a complete redesign.
   - First:
     - inspect the **current** implementation of a module, including its tests,
       example scripts, Docker setup, and Colab notebooks,
     - understand what has already been refactored or stabilized,
     - preserve any logic that is already documented and validated.
   - Prefer:
     - **local refactors**,
     - adding small helper functions,
     - strengthening input validation and error handling,
     - adding or improving tests and documentation,
     - removing or merging obviously redundant fragments.

2. **Scientific correctness, reproducibility, and determinism**
   - Target Python 3.11+ with **full type hints** and compatibility with:
     - `black`, `isort`, `ruff`,
     - strict `mypy` (avoid `Any` unless strictly necessary).
   - Randomness:
     - expose `random_state`/RNG parameters in public APIs and CLIs,
     - ensure deterministic results for fixed inputs and seeds,
     - document any inherently stochastic elements and their expected variability.
   - Use numerically stable methods (e.g. log-sum for probabilities/scores, careful
     handling of zero/near-zero denominators, well-defined NaN handling).

3. **Safety, clarity, and simple CLIs**
   - Never use `eval`/`exec` or execute code from unvalidated paths/files.
   - Error messages must:
     - clearly state what is wrong (inputs, shapes, missing columns, parameter ranges),
     - avoid silent “fixups” of user data without explicit messages or warnings.
   - Design CLIs for microbiology/bioinformatics users:
     - keep required arguments minimal,
     - document all critical parameters and defaults explicitly,
     - surface clear `--help` messages.

4. **Respect for existing production code**
   - Treat modules and functions that are already used in examples, Docker images,
     and notebooks as **production code**:
     - do not change their behaviour or public API lightly,
     - if changes are required, keep them **backwards compatible** whenever possible,
     - if a breaking change is unavoidable, update:
       - all CLIs,
       - all Dockerfiles and docker-compose definitions,
       - all Colab/notebook examples,
       - all documentation and quick-start guides,
       - all tests that depend on this API.
   - Always prefer:
     - adding new, clearly named functions rather than breaking existing ones,
     - wrapping legacy behaviour in thin adapters if needed.

---

## Agent workflow and strategy

1. **Before making changes**
   - Discover and map:
     - existing modules, packages, and CLIs under `separated_repos`,
     - current tests (`tests/`, `*_test.py`, `test_*.py`),
     - test harnesses and meta-scripts (`verify_all_modules.py`,
       `test_functionality.py`, `test_network_analysis.py`, etc.),
     - notebooks and Colab variants,
     - Docker and docker-compose files used to run each module.
   - Identify:
     - which elements are already refactored and in active use,
     - which files are clearly outdated duplicates, prototypes, or dead code,
     - where there are obvious gaps in tests, documentation, or coverage.

2. **Change planning**
   - **Before editing files**, outline a short plan:
     - which files will be modified,
     - the goal of each change (e.g. “add CLI smoke test”, “remove dead helper”,
       “align Docker entrypoint with current CLI”),
     - potential risks (e.g. API change affecting Docker and notebooks).
   - Prioritize:
     - closing small, well-defined gaps end-to-end (e.g. “fully test and validate
       one CLI across all three variants: local, Docker, Colab”),
     - over scattering small edits throughout the entire repository.

3. **Implementation priorities**
   - First:
     - strengthen or add unit and integration tests,
     - improve API consistency (parameter naming, types, return structures),
     - remove or merge clearly redundant, never-imported, or superseded files
       once their content has been migrated.
   - For any change:
     - keep track of all affected execution variants:
       - library API,
       - CLI scripts,
       - Docker image entrypoints,
       - Colab and other notebooks,
       - verification scripts (`verify_all_modules.py`).
     - update them in sync.

4. **Post-change verification**
   - ALWAYS:
     - run or define tests that exercise all changed code paths,
     - for each modified module, ensure at least:
       - unit tests for core logic,
       - a smoke test that covers:
         - CLI invocation,
         - Docker-based run (image build + minimal run where feasible),
         - Colab or notebook-based run (at least a headless/scripted execution path).
   - If end-to-end execution of a Docker or Colab variant is too heavy for routine
     test suites, provide:
     - a clear, scripted reproduction (commands or CI job definition),
     - and a separated “slow” or “integration” test group that can be run manually
       or in nightly CI.

---

## Repository-wide maintenance obligations

1. **Naming and entry points**
   - Enforce consistent naming, especially:
     - `Phylogenetic` (never `Phylgenetic`, `Phylotrait`, etc.).
   - On any rename of a function/module/class:
     - update all related:
       - CLI entrypoints (e.g. `registry.py`, `pyproject.toml`),
       - documentation, README, quick-start guides,
       - examples and notebooks,
       - tests.
   - Ensure that every CLI or entrypoint documented in the repo:
     - maps to an existing, importable module,
     - exposes a runnable main function,
     - has at least one smoke test (unit, CLI, Docker, or notebook).

2. **Documentation alignment and consolidation**
   - Remove duplication:
     - when two files describe the same workflow (e.g. a quick start and a summary),
       merge the content into one primary source,
       deprecate or delete the superseded one after migration.
   - Keep consistent:
     - module names,
     - dataset names and example file paths,
     - CLI examples (arguments, flags, file paths, environment assumptions).
   - Fix:
     - inconsistent step numbering in quick starts,
     - mismatched deployment modes (local vs Docker vs Colab) across documents.

3. **Automated validation and coverage**
   - Convert ad-hoc scripts (e.g. `test_functionality.py`,
     `test_network_analysis.py`) into structured `pytest` suites with:
     - proper assertions (not just print statements),
     - parameterized tests where appropriate,
     - fixtures for shared data and example inputs.
   - Ensure that the central verification driver (e.g. `verify_all_modules.py`
     or successor) checks, for **every module and its variants**:
     - importability,
     - at least one typical run on small, synthetic or example data,
     - clear, module-specific error messages on failure.

---

## Testing, analysis, and benchmarking expectations

### Target coverage and execution variants

- For each module under `separated_repos`, the agent should aim for:
  - **100% test coverage** (line and branch where feasible) for:
    - core library functions,
    - critical algorithms and numeric routines,
    - error-handling for invalid inputs.
  - Full coverage of **all three execution variants**, where applicable:
    - CLI,
    - Docker,
    - Colab/notebook.
- For each variant:
  - provide at least one automated smoke test:
    - CLI: unit-level or `subprocess` tests with synthetic inputs,
    - Docker: build + minimal run test (or CI job definition),
    - Colab/notebook: headless execution or a robust CI-driven test harness.

> When full 100% coverage is temporarily not feasible (e.g. external tools,
> heavy pipelines), the agent must:
> - explicitly document which parts are excluded,
> - justify the exclusion (I/O-heavy, external dependency, etc.),
> - add TODO markers with concrete steps to close the gap later.

### Current test coverage limitations (to be resolved)

- Existing scripts such as `test_functionality.py` and `test_network_analysis.py`:
  - use ad-hoc print-based checks instead of structured `pytest` tests,
  - do not support reliable coverage reporting or CI gating,
  - primarily validate that imports succeed and functions “run”,
    without asserting numerical correctness over parameter ranges.
- Notebook and Docker checks:
  - often verify only file presence or keywords,
  - do **not** execute notebooks end-to-end,
  - do **not** build or run images, so runtime regressions can slip through.

### Missing mathematical validation

- Core numerical modules for:
  - clustering,
  - MDR and AMR analysis,
  - phylogenetic workflows,
  - network metrics and report generation,
  currently lack:
  - deterministic, reference-based tests (e.g. comparisons against analytic solutions,
    SciPy/NumPy/scikit-learn baselines),
  - boundary and invariance tests (symmetry, monotonicity, stability under
    resampling/bootstrap where applicable).
- The agent must introduce:
  - mathematical regression tests for each statistical routine
    (entropy, Cramér’s V, information gain, cluster quality, network metrics),
  - synthetic datasets with known, analytically tractable answers,
  - tests for invariants (e.g. symmetry of distance matrices, non-negativity,
    probability sums to 1, PD properties).

### Uncovered execution variants

- CLI wrappers (e.g. `run_cluster_analysis.py`, `run_mdr_analysis.py`,
  `run_phylogenetic_analysis.py`, `verify_all_modules.py`):
  - are not comprehensively tested for argument parsing, I/O, and error handling.
- Colab notebooks:
  - are not executed end-to-end in automated tests.
- Docker and docker-compose:
  - are parsed or documented but often not built and smoke-tested,
  - may hide dependency drift or broken entrypoints.

The agent must:
- add `pytest`-driven tests that exercise each execution pathway:
  - library API,
  - CLI,
  - Docker image,
  - Colab/notebook (where practically testable),
- provide clear instructions or CI snippets to build and run Docker images,
- add at least smoke tests for notebook execution or a dedicated tool to convert
  notebooks into runnable scripts for testing.

### Benchmarks and performance safeguards

- Currently there are no systematic performance or scalability benchmarks for:
  - large matrices (e.g. MIC/AMR binaries),
  - graph/network analytics,
  - multiprocessing pathways.
- The agent should:
  - introduce **lightweight performance benchmarks** (e.g. via `pytest-benchmark`)
    for critical functions (association rule mining, clustering, centrality),
  - track simple timing/resource baselines to detect severe regressions,
  - keep these benchmarks optional/slow, but documented and runnable.

---

## Module-specific requirements

(Adapt paths and filenames to the actual repository layout; the conceptual
requirements remain.)

- **strepsuis-amrpat**
  - Co-occurrence matrices:
    - must be **symmetric**, with a clearly defined diagonal
      (e.g. counts or self-co-occurrence).
  - Association metrics:
    - support, confidence, lift, p-values,
    - consistent types (floats, no magic strings containing numbers),
    - transparent formulas and assumptions, tested against baselines.
  - Multiple testing:
    - FDR (e.g. Benjamini–Hochberg) clearly implemented and documented,
    - both raw and adjusted p-values reported.
  - Where applicable:
    - bootstrap or permutation-based confidence intervals,
    - explicit `random_state` handling.

- **strepsuis-amrvirkm**
  - K-modes:
    - sensible default parameters,
    - implemented and tested k selection strategy
      (e.g. silhouette, elbow, or comparable criterion).
  - MCA:
    - report explained variance,
    - expose loadings/coefficient structures for interpretation.
  - Cluster interpretation:
    - provide summaries of AMR/virulence prevalence per cluster,
    - export ready-to-publish tables where possible.

- **strepsuis-genphennet**
  - Mutual information / entropy:
    - numerically stable and comparable to established implementations
      (e.g. scikit-learn),
    - configurable estimation strategy (binning, kNN) where appropriate.
  - Networks:
    - community detection must report modularity,
    - basic centrality metrics (degree, betweenness, etc.) available and tested.
  - Edge filtering:
    - allow thresholding on strength, significance, or both,
    - clearly document default thresholds.

- **strepsuis-phylotrait**
  - Faith’s PD and related metrics:
    - align with scikit-bio conventions where feasible,
    - document exact definitions, units, and assumptions.
  - Tree-aware clustering:
    - tests must verify that, on synthetic/example data:
      - mean within-cluster phylogenetic distances <
        mean between-cluster distances.
  - Input robustness:
    - handle missing tips gracefully,
    - support mapping between isolate/sequence identifiers and tree labels.

- **strepsuis-genphen**
  - Orchestration and integration:
    - by default **preserve all strains/features** unless filters are explicitly
      enabled by the user,
    - surface clear logging or summaries of:
      - which filters were applied,
      - how many strains/features were removed at each step.
  - Determinism:
    - identical inputs + identical parameters → identical outputs
      across all variants (library, CLI, Docker, Colab).
  - Transparency:
    - allow exporting intermediates (input matrices, networks, clustering
      results) for inspection and re-analysis.

---

## Output, reporting, and example artefacts

1. **API and docstrings**
   - Every **public** function, class, and CLI:
     - has a clear, complete docstring:
       - purpose,
       - arguments and their types,
       - return types,
       - assumptions, caveats, and limitations,
       - references to relevant scientific literature where appropriate.
     - includes a minimal usage example if possible.
   - Internal helper functions:
     - may use shorter docstrings, but still describe inputs and outputs clearly.

2. **Result formats**
   - Tabular outputs:
     - tidy `CSV`/`TSV` as the primary format (one main table per file),
     - optional multi-sheet Excel (`.xlsx`) for workflows that naturally produce
       multiple tables.
   - Plots:
     - always export `SVG` or `PDF` for publication,
     - plus high-resolution `PNG` for quick inspection,
     - ensure:
       - labelled axes with units,
       - clear legends,
       - sensible titles/subtitles,
       - colourblind-friendly palettes.
   - HTML reports:
     - should be self-contained when possible (embedded assets) or accompanied
       by clear instructions for any external dependencies.

3. **Preservation and placement of example analyses**
   - The agent must:
     - preserve exact outputs for example analyses in the repo:
       - CSV/TSV result files,
       - HTML reports,
       - image files (PNG/SVG/PDF),
       - any other artefacts referenced in documentation/notebooks.
     - ensure these artefacts are:
       - stored in logically named directories (e.g. `examples/`, `results/`,
         `docs/examples/`),
       - clearly referenced from README, quick starts, and notebooks,
       - documented in terms of:
         - input data,
         - commands/notebook cells used to generate them,
         - how to interpret the outputs.
   - Where helpful:
     - add **annotated screenshots** (PNG) demonstrating:
       - how to provide inputs,
       - how to run the analysis (CLI, Docker, Colab),
       - how to interpret key parts of the output.
     - accompany screenshots with concise step-by-step text descriptions.

4. **Change summaries**
   - After a substantial set of modifications, the agent should prepare a brief,
     technical summary covering:
     - what has changed and why,
     - how dependencies were aligned (between `pyproject.toml` and
       `requirements*.txt`),
     - which naming and entrypoint issues were fixed,
     - which tests were added or improved, and how coverage increased,
     - any new mathematical validation or benchmarks.
   - Avoid marketing language:
     - do **not** use claims like “revolutionary”, “best-in-class”, or
       “production-ready”.
   - Use a neutral, scientific tone, suitable for future inclusion in
     high-quality technical documentation or academic methods sections.
