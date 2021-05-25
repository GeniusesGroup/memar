# sRPC - Application Protocol
sRPC application protocol is most efficient RPC(remote procedure call) as simple as Function idea! It is also messaging protocol with simplest structure you seen ever. Response and request header have same header structure! we suggest use syllab encoder to encode/decode payload data but it can work with other encoders too! Also we strongly suggest transfer it standalone above network protocols but it can transfer by including to other application protocol like HTTP!

## Goals
- minimum overhead to find service from server services
- minimum data exchange forces by protocol

## Not Goals
- Easy to read and write by human!

## Packet architecture
| bit     | Length(byte-Octet) | Data                   |
| ---     | :---:              | :---:                  |
| 0       | 8                  | Service ID or Error ID |
| 64      | ~                  | Payload                |

### Service ID
- It is on request packet and use to route service and call the handler!
- Read more about ServiceID [here](./Giti-Service.md)

### Error ID
- It is on response packet and use to show if calling service occur an error!
- Read more about ErrorID [here](./Giti-Error.md)

### Payload
Can be any encoded data in any format with any length that service force to accept it on its specs! Anyway we strongly suggest use [Syllab](./Syllab.md) due to it is most efficient data encoder!

## Supported programming languages
It is so simple protocol that can easily encode and decode in any programming language! We implement it on some language like [C](), [Go](https://github.com/SabzCity/libgo/blob/master/srpc), [JavaScript]() and more in progress ...
