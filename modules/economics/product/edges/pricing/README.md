# Pricing

## Model

- `(product)-[:pricing]->(count_unit)` (note: rule)
- `(rule)-[:process_pricing_for]->(product)`

## Decisions from Organization ideas backlog (2026-09-16)

- **Pricing is a module family, not one module.** A transportation service's price varies by city, hour, route, zone, demand — hundreds of independently evolving pricing modules for one organization (Uber example), all attached to the Product level while invoice-level rules (zeroing a user's bill) are a *different* level: an Invoice-level rule making the payable zero does not make the service's price zero. *(decided)*
