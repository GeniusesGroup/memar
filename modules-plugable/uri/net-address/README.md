# Communication Address
Addresses are used to identify both the sender and the intended receiver(s). The addresses are carried in the header area of the bitstrings, allowing the receivers to determine whether the bitstrings are of interest and should be processed or should be ignored. A connection between a sender and a receiver can be identified using an address pair (sender address, receiver address). Usually, some address values have special meanings. An all-1s address could be taken to mean an addressing of all stations on the network, so sending to this address would result in a broadcast on the local network. The rules describing the meanings of the address value are collectively called an addressing scheme.

## Model

- `(connection)-[:net_address_is]->(uri(text))`
- `(uri(text))-[:net_address_for]->(connection)`
