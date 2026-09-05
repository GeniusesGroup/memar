# Count Unit
Count uint or [count interface]() or [Classifier](https://en.wikipedia.org/wiki/Classifier_(linguistics)) ([In persian](https://fa.wikipedia.org/wiki/%D8%B1%D8%A7%D8%A8%D8%B7_%D8%B4%D9%85%D8%A7%D8%B1%DB%8C)) or [measure word](https://en.wikipedia.org/wiki/Measure_word) or [unit of measurement](https://en.wikipedia.org/wiki/Unit_of_measurement)

## Examples

- currency, Hz, core / gram, liter, ...


<!--
https://en.wikipedia.org/wiki/International_System_of_Units
e.g. Hz, core, gram, liter, number, ...
CountUnit
MetricUnit
-->

## Model

- `(thing)-[:count_unit_is]->(count_unit)`
- `(count_unit)-[:is_count_unit_for]->(thing)`

## Policies (rules)

- Almost all `thing` MUST have just one `count_unit` such as
- a `money` unit like `us-dollar` for economic `account`
- a `metric unit` like `litre` for any `good` as a `product`
