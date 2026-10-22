# Page
Page is an addressable composition of widgets with state and history, a core part of `computer/ui`: core domains need it as they need Service, so it is not pluggable (owner, 2026-10-22). Home: `modules/computer/ui/page`. A page belongs to the domain whose subject it is, in that domain's `ui` folder; pages with no settled domain wait in `modules-plugable/gui`.

## Model
- `(software)-[:---]->(software_gui_page)`
