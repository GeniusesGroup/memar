# Coordinate GPS

## Model

- `(thing)-[:coordinate_gps_at]->(time)`
- `(thing)-[:coordinate_gps_on]->(boundary_gps)`

## Policies (rules)

- use `coordinate_...` to get physical location.
- It CAN set by electronic device or some authorized user.
- It CAN be very long time same location or very short moving thing.
