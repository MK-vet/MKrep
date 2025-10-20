# MKrep Tool Portal Guide

## Overview

The MKrep Tool Portal is an interactive documentation website that provides easy access to all analysis tools for external users, especially researchers reading scientific articles.

## Portal URL

**🌐 [https://mk-vet.github.io/MKrep/](https://mk-vet.github.io/MKrep/)**

## Portal Structure

### Main Landing Page (`docs/index.html`)
- Overview of all 5 analysis tools
- Quick access buttons to run tools in Google Colab
- Links to documentation, demo data, and example results
- Prominent badges showing production-ready status
- Feature highlights and key capabilities

### Tool-Specific Pages (`docs/tools/`)
Each of the 5 analysis tools has a dedicated page:

1. **Cluster Analysis** (`cluster-analysis.html`)
   - K-Modes clustering for MIC, AMR, and virulence data
   - Statistical methods, input requirements, output formats
   - Quick start options (Colab, Local, CLI)

2. **MDR Analysis** (`mdr-analysis.html`)
   - Multi-drug resistance pattern analysis
   - Co-resistance networks and association rules
   - Bootstrap prevalence estimation

3. **Network Analysis** (`network-analysis.html`)
   - Statistical network analysis of feature associations
   - Chi-square tests, information theory metrics
   - 3D network visualization

4. **Phylogenetic Clustering** (`phylogenetic-clustering.html`)
   - Tree-based clustering with evolutionary context
   - Faith's Phylogenetic Diversity
   - UMAP dimensionality reduction

5. **StrepSuis Analysis** (`strepsuis-analysis.html`)
   - Specialized analysis for *Streptococcus suis*
   - Ensemble clustering with comprehensive trait profiling
   - Association rules and MCA visualization

### Demo Data Page (`docs/demo-data/`)
- Direct download links for all example CSV files
- File format requirements and guidelines
- Complete dataset bundle option
- Usage instructions for Colab and local installation

### Results Gallery (`docs/results/`)
- Example outputs from each analysis tool
- Descriptions of generated reports (HTML, Excel, PNG)
- Links to run tools yourself
- Interpretation guides

## Features for External Users

### 🎯 Quick Access
- One-click buttons to launch tools in Google Colab
- No installation or setup required
- Direct links from scientific articles to tool pages

### 📊 Transparent Demonstrations
- Example results showing what to expect
- Pre-generated reports available for review
- Demo datasets ready to download and test

### 📚 Comprehensive Documentation
- Detailed tool descriptions
- Statistical methods explained
- Input/output specifications
- Runtime estimates and parameter defaults

### 🚀 Multiple Deployment Options
Each tool page offers:
1. **Google Colab** - No installation, run in browser
2. **Local Installation** - Full control and customization
3. **Command Line Interface** - Automation and scripting
4. **Interactive Dashboard** - User-friendly GUI (Voilà)

## Portal Deployment

### GitHub Pages Setup
The portal is automatically deployed via GitHub Actions workflow (`.github/workflows/pages.yml`):
- Triggers on push to main branch
- Deploys `docs/` directory to GitHub Pages
- Available at https://mk-vet.github.io/MKrep/

### Local Testing
To test the portal locally:
```bash
cd docs
python -m http.server 8000
# Open http://localhost:8000 in browser
```

### Configuration
- `docs/_config.yml` - Jekyll configuration for GitHub Pages
- `docs/README.md` - Documentation about the portal structure

## Benefits for Scientific Publishing

### For Authors
- Provide readers direct access to analysis tools
- Include portal URL in Methods section
- Demonstrate reproducibility and transparency
- Enable readers to replicate analyses

### For Readers
- Understand tool capabilities before using
- Run analyses without complex setup
- Access example data and results
- See exactly what outputs to expect

### For Reviewers
- Verify analysis methodology
- Test tools with demo data
- Assess code quality and documentation
- Check reproducibility claims

## Usage in Scientific Articles

### Methods Section
```
"All analyses were performed using MKrep tools (https://github.com/MK-vet/MKrep).
Interactive tool demonstrations and example results are available at
https://mk-vet.github.io/MKrep/. Specific tools used include..."
```

### Supplementary Materials
```
"Analysis tools and demo data are available through the MKrep tool portal
(https://mk-vet.github.io/MKrep/). Each tool provides one-click access
via Google Colab, requiring no local installation."
```

### Code/Data Availability
```
"Analysis code: https://github.com/MK-vet/MKrep
Interactive tools: https://mk-vet.github.io/MKrep/
Demo data: Available through the tool portal demo-data section"
```

## Portal Maintenance

### Adding New Tools
1. Create HTML page in `docs/tools/[tool-name].html`
2. Add tool card to `docs/index.html`
3. Create results page in `docs/results/[tool-name].html`
4. Update results index with new tool

### Updating Content
- Edit HTML files directly in `docs/` directory
- Changes automatically deployed via GitHub Actions
- Test locally before pushing to main branch

### Adding Example Results
1. Run analysis with demo data
2. Save outputs (HTML, Excel, PNG)
3. Upload to repository or external hosting
4. Link from results pages

## Technical Details

### Technologies Used
- **HTML5** - Modern semantic markup
- **Bootstrap 5** - Responsive CSS framework
- **Font Awesome** - Icon library
- **GitHub Pages** - Static site hosting
- **GitHub Actions** - Automated deployment

### Browser Compatibility
- Chrome, Firefox, Safari, Edge (latest versions)
- Mobile responsive design
- Works without JavaScript (progressive enhancement)

### Accessibility
- Semantic HTML structure
- ARIA labels where appropriate
- Keyboard navigation support
- High contrast color schemes

## Future Enhancements

### Planned Features
- [ ] Add Binder deployment option for Jupyter notebooks
- [ ] Embed live demo results in results pages
- [ ] Add video tutorials for each tool
- [ ] Create interactive parameter calculator
- [ ] Add citation generator for each tool
- [ ] Implement search functionality
- [ ] Add user feedback form

### Integration Opportunities
- Link to preprint/publication when available
- Connect to data repositories (Zenodo, Figshare)
- Integration with workflow platforms (Galaxy, CWL)
- API documentation for programmatic access

## Support and Feedback

### Reporting Issues
- Use GitHub Issues for bug reports or enhancement requests
- Include specific page URLs and browser information
- Screenshots helpful for layout issues

### Contributing
- Fork repository and submit pull requests
- Follow existing HTML/CSS structure
- Test locally before submitting
- Update this guide for significant changes

## License

The portal is part of the MKrep project, licensed under MIT License.
Content and documentation are freely available for use and modification.

---

**Last Updated:** 2025-10-17  
**Portal Version:** 1.0.0  
**Status:** Production Ready ✅
