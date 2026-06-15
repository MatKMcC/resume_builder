 # Resume Builder TODO
 
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

### In Progress
- [ ] Friction analysis framework real job applications 📅 2026-04-03 #job-applications #user-research
- [ ] Add Sevi's resume for learning / building experience

### Resume Compatibility
- [ ] Functionality to update older resumes to new formats
- [ ] Integrate resume into a UI
- [ ] Add resume versions control to resumes 📅 2026-04-03 #versioning 
- [ ] Add Compatibility for educational details

### Usability
- [ ] API service provided
- [ ] CLI provided

### Github Integration
- [ ] Run test on github pushes
- [ ] Set up monitoring to make sure no PII is leaked in resume / resume history 2026-04-03 #pii #testing #python

### Comprehensive Testing Suite

## Completed ✅
- [x] \[Template\]Created LaTeX template system with Jinja2 ✅ 2026-03-15  
- [x] \[PDF\] Implemented basic PDF generation workflow ✅ 2026-03-18
- [x] \[Testing\]Resume test that confirms that specific sections are implemented in resume #testing #python 📅 2026-04-03 ✅ 2026-04-03
- [x] \[Testing\] Resume test that confirms that the resume structure is valid #testing #python 📅 2026-04-03 ✅ 2026-04-03
- [x] \[Testing\] Resume Test that confirms that the resume has correct metadata information #testing #python 📅 2026-04-03 ✅ 2026-04-03
- [x] \[Testing\] Template test that template is built correctly ✅ 2026-06-09
- [x] \[Resume\] Built JSON resume structure ✅ 2026-03-08
- [x] \[Resume\] Update resumes to YAML files not JSON files 📅 2026-04-03 #yaml ✅ 2026-06-09
- [x] \[Resume\] Remove highlights sections in the resumes to improve functionality / readability 📅 🔼 ✅ 2026-06-09 #resume 
- [x] \[Resume\] Add function to update resumes to newer versions 📅 2026-04-03 ✅ 2026-06-09 #versioning
- [x] \[Resume\] Add resume versions control to resume_builder 📅 2026-04-03 ✅ 2026-06-09 #versioning 
- [x] \[Workflow\] Set up Obsidian project management system ✅ 2026-03-20
- [x] \[Workflow\] Scrub PII from existing github repository #resume #PII 📅 2026-04-02 ✅ 2026-04-03
- [x] \[Workflow\] Set up a github repository for resume and versions 📅 2026-06-09 #git #workflow ✅ 2026-06-09
- [x] \[Workflow\] Make resume_builder an executable package 📅 2026-04-03 ✅ 2026-06-09 #versioning
- [x] \[Resume\] Create new resume template for previous resume design

