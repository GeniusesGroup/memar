## Media Type Extension
Want a protocol to declare global service, error, ... in any language with desire goals, So we decide to add new main-type to media-type URI scheme instead invent from scratch. Add new top-level type names (main-type) as `domain` instead of `application` to have proper way to indicate domain specific media types.

## Structure
`type "/" [tree "."] subtype ["+" suffix]* [";" parameters]`   
`domain/{{domain-name}}. {{structure-type}} +{{codec-type}} ;{{structure-name}}`   
`domain/sabz.city.storage+syllab; quiddity`
- **domain-name** as a tree for a organization by its domain name.
- **structure-type** or structure scope like `storage`, `service`, `error`, `page`, `widget`, ...
- **codec-type** like `syllab`, `json`, `xml`, `protobuf`, `flatbuf`, `html`, ...
- **structure-name** must be unique in the domain scope e.g. "product" in the "page" scope of the domain. e.g. `log`, `get-email`, `get-email`, `request`, `response`, `not-standard-structure-id`, ... Due to RFC rules, a media-type can has more than one parameters, so you can easily add more than one if need it like http that use `charset=` and `boundary=` in content-type header.

## ID
- To have canonical structure IDs calculate it from hash of MediaType().
- ID is first 64bit of SHA3-256 hash of structure that transfer in base64 if protocol is string base.
- Zero ID means no data structure e.g. no error, ....

## Goals
- Easily generate SDK in any programing language
- Transfer and retrieve by ID in any protocol
- Store locale detail not just english detail
- 

## Other ways
- use URN standard like `urn:giti:sabz.city:page:login` as `urn:giti:{{domain-name}}:{{structure-type}}:{{structure-name}}`

## RFCs
- https://datatracker.ietf.org/doc/html/rfc6838
- https://datatracker.ietf.org/doc/html/rfc2046
- https://datatracker.ietf.org/doc/html/rfc2609

## Resources
- https://en.wikipedia.org/wiki/Media_type
