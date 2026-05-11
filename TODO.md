 # Resume Builder TODO

## Current Sprint (March 30 - April 3, 2026)

### Action Items
- [ ] End to End test that test that confirms that a resume.json creates an expected latex file  📅 2026-04-03 #testing #python
- [ ] End to End test that test that confirm that a resume.json creates a PDF  📅 2026-04-03 #testing #python
- [ ] Add resume versions control to resume_builder 📅 2026-04-03 #versioning 
- [ ] Add function to update resumes to newer versions 📅 2026-04-03 #versioning 
- [ ] Set up a github repository for resume and versions 📅 2026-04-03 #git #workflow 
- [ ] Add resume versions control to resumes 📅 2026-04-03 #versioning 
- [ ] Update resumes to YAML files not JSON files 📅 2026-04-03 #yaml
- [ ]  Remove highlights sections in the resumes to improve functionality / readability 📅 🔼  #resume
- [ ] Set up friction analysis framework real job applications 📅 2026-04-03 #job-applications #user-research
- [ ] Test resume and template compatibility 📅 2026-04-03 #testing #python
- [ ] Set up monitoring to make sure no PII is leaked in resume / resume history 2026-04-03 #pii #testing #python
## Goals

### Resume Compatibility
- [ ] Backward compatible with older resumes for rebuilds
- [ ] Functionality to update older resumes to new formats
- [ ] Integrate resume into a UI

### Template Compatibility
- [ ] Templates should be compatible with specified resume versions

### Usability
- [ ] Integration with github
- [ ] API service provided
- [ ] CLI provided

### Comprehensive Testing Suite
- [ ] Test resumes should never fail a resume build for all templates available
- [ ] Every resume and template should be backward compatible
- [ ] Build on github pushes

## Completed ✅
- [x] Built JSON resume structure ✅ 2026-03-08
- [x] Created LaTeX template system with Jinja2 ✅ 2026-03-15  
- [x] Implemented basic PDF generation workflow ✅ 2026-03-18
- [x] Set up Obsidian project management system ✅ 2026-03-20
- [x] Resume test that confirms that specific sections are implemented in resume #testing #python 📅 2026-04-03 ✅ 2026-04-03
- [x] Resume test that confirms that the resume structure is valid #testing #python 📅 2026-04-03 ✅ 2026-04-03
- [x] Resume Test that confirms that the resume has correct metadata information #testing #python 📅 2026-04-03 ✅ 2026-04-03
- [x] Scrub PII from existing github repository #resume #PII 📅 2026-04-02 ✅ 2026-04-03

## Decisions Made
- **Data Format:** YAML for structured resume data (flexible, version controlled and readable)
- **Templates:** LaTeX via Jinja2 (professional output, programmable, easily read)
- **Project Management:** Obsidian with symlinked files (AI-accessible, cross-project)
- **Versioning:** Metadata in YAML + git for code versioning

## Questions/Research Needed
- Best practices for YAML schema evolution and backward compatibility?
- How to handle resume variants efficiently (git branches vs file variants)?  
- What's the optimal application tracking granularity?
- Which job posting APIs have the best data quality and availability?
