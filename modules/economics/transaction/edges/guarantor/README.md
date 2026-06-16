# Guarantor
Guarantor or endorsement in law indicate that someone who promises to pay a debt if the person who should pay it does not.

## Dictionary
guarantor   
guar·an·tor /ˌgærənˈtɔː US -ˈtɔːr/ n [C]   
- law someone who promises to pay a debt if the person who should pay it does not
- n.  one who provides a warrant or guarantee to another

## Graph
- `(transaction)-[:guarantor_is]->(transaction)`
- `(transaction)-[:is_guarantor_for]->(transaction)`

- `(User)-[:GUARANTEES]->(transaction {status: 'Active'})`

## Policy (rule)
- a `transaction` CAN have more than one `guarantor`
- TODO::: how process more than one `guarantor`? FIFO??

## Fields
