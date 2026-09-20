# IMEI
Serial numbers are identification numbers given to one product in particular, to allow to track the history of the item from reception to delivery and after-sales. e.g. https://en.wikipedia.org/wiki/International_Mobile_Equipment_Identity

## Model

- `(thing)-[:imei_is]->(uri(text))`
- `(uri(text))-[:imei_for]->(thing)`

## Policies (rules)

- `international mobile equipment identifier` a number that each mobile phone has, which it sends whenever someone uses it to make a phone call
- thing MUST have `mobile phone` label before get this relation??
- Or every thing that get this label KNOWN as mobile phone??
- Other device types like IoT devices CAN get this label??
