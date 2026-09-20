# Page

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Page types - edges/page.go
- **Idea**: page kinds Service, Landing, Content, Email, Print.
- **Review questions**: closed set or organizational-open? Is Print a page kind or a rendering target?

### Page code - edges/code/protocol/data_model.go
- **Idea**: GUICategories interface: Content (HTML), Style (CSS), Logic (JS).
- **Review questions**: naming (GUI categories under page/code) and whether this triple is a projection-layer concern rather than domain data.