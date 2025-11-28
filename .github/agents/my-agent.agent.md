---
# Fill in the fields below to create a basic custom agent for your repository.
# The Copilot CLI can be used for local testing: https://gh.io/customagents/cli
# To make this agent available, merge this file into the default repository branch.
# For format details, see: https://gh.io/customagents/config

name:
description:
---

# GitHub Copilot Agent — Custom Instructions for the StrepSuis Suite

**Use these directives as the agent's persistent custom instructions (not a one-off prompt) when working on https://github.com/MK-vet/MKrep/tree/main/separated_repos.** They define mandatory behaviour for the initial public release of all five modules: strepsuis-amrpat (AMR association and networks), strepsuis-amrvirkm (K-modes/MCA clustering), strepsuis-genphennet (mutual-information networks), strepsuis-phylotrait (phylogeny/trait integration), and strepsuis-genphen (cross-module orchestration).

## Core principles
- Prioritise scientific correctness, reproducibility, transparency, robustness, and publication-grade outputs over convenience.
- Target Python 3.11+ with full type hints and modular design that is black/isort/ruff/strict mypy compliant. Avoid marketing terms such as “new” or “production-ready.”
- Make randomness explicit (seeds and RNG objects). Prefer numerically stable methods to clever but opaque shortcuts.

## Behavioural expectations
- **Validation first:** Write or update tests alongside code. Cover edge cases (empty inputs, single rows/columns, zero variance, duplicated IDs, missing values, extreme values) and synthetic ground truth (perfect association/independence, known clusters, symmetric co-occurrence, known communities). Keep default tests fast; mark heavy workloads as slow.
- **Fail fast and safely:** No silent failures. Emit actionable errors. Avoid unsafe eval/exec and unvalidated file paths. Keep CLIs simple for microbiology users who may not be software engineers.
- **Determinism and packaging:** Pin and align dependencies across `python_package/pyproject.toml` and `requirements.txt`. Ensure CLI registry entries in `python_package/mkrep/analysis/registry.py` map to importable modules and correct extras.

## Repository-wide cleanup obligations
1. **Naming and entry points**
   - Enforce consistent phylogenetic naming (`Phylogenetic`, never `Phylgenetic`) across filenames, commands, docs, and examples.
   - Verify every advertised module in README/quick-start docs maps to an existing, runnable script/CLI entry point.

2. **Documentation consolidation**
   - Resolve duplicated Quick Start numbering and keep option labels aligned with supported deployment modes.
   - Merge overlapping guides/summaries; retire superseded files once content is preserved.
   - Keep module names, datasets, and command examples consistent across README, quick-starts, and module summaries.

3. **Validation and coverage**
   - Extend runtime coverage beyond static checks: add smoke/integration tests for modules lacking them and integrate with CI or `verify_all_modules.py`.
   - Ensure `test_functionality.py` (or its successor) validates importability, CLI entry points, and baseline execution paths for every module.

## Module-specific requirements
- **strepsuis-amrpat:** Symmetric co-occurrence matrices; association metrics (support, confidence, lift, p-values) internally consistent with enforced FDR thresholds; bootstrap CIs where applicable.
- **strepsuis-amrvirkm:** Robust K-modes defaults with k selection (silhouette/elbow); MCA exposes explained variance and loadings; interpret clusters via AMR/virulence prevalence.
- **strepsuis-genphennet:** Mutual information and entropy stable and comparable to scikit-learn; network/community routines expose modularity and centrality metrics.
- **strepsuis-phylotrait:** Faith’s PD and related metrics match scikit-bio conventions; tree-aware clustering yields lower within-cluster than between-cluster phylogenetic distances.
- **strepsuis-genphen:** Preserve all strains/features unless explicitly filtered; orchestrated workflows remain deterministic and transparent.

## Output standards
- Every public function and CLI command carries a clear docstring (purpose, arguments, return types, assumptions, caveats, references).
- Prefer outputs ready for scientific use: tidy CSV/TSV or multi-sheet Excel; vector graphics (SVG/PDF) plus high-res PNG with labelled axes/legends and colourblind-safe palettes; self-contained HTML reports when appropriate.
- Provide concise change summaries covering dependency alignment, naming normalization, documentation consolidation, and validation/coverage updates—without marketing phrasing.
