# Repository Rename Plan

## Current State
- Main repository: `MK-vet/MKrep`
- Branch: `main`

## Planned Changes

### Main Repository
- New name: `MK-vet/StrepSuis_Suite`
- When: Before public release

### Individual Tool Repositories
These will be created as NEW repositories (not renamed):
- `MK-vet/strepsuis-amrpat`
- `MK-vet/strepsuis-amrvirkm`
- `MK-vet/strepsuis-genphen`
- `MK-vet/strepsuis-genphennet`
- `MK-vet/strepsuis-phylotrait`

## Steps for User (Manual)

1. **Rename main repository** on GitHub:
   - Go to Settings > Repository name
   - Change `MKrep` to `StrepSuis_Suite`
   - GitHub will set up automatic redirects

2. **Update local clones:**
   ```bash
   git remote set-url origin https://github.com/MK-vet/StrepSuis_Suite.git
   ```

3. **Create individual repositories** for each tool:
   - Use GitHub UI: New Repository
   - Copy content from `separated_repos/TOOLNAME/`
   - Follow DEPLOYMENT_GUIDE.md for each tool

## No Action Required for Documentation
All documentation already uses correct names and is ready for the rename.
