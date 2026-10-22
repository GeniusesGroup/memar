# Widget
Widget is a named, stateful aggregator of services and of other domains' widget contracts, hosted by software; core domains need it, so it is a core part of `computer/ui` and not pluggable (owner, 2026-10-22). It is not bound to the screen. Home: `modules/computer/ui/widget`.

## Model
- `(software)-[:---]->(software_gui_widget)`
