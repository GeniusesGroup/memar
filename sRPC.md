# sRPC - Application Protocol
sRPC application protocol is most efficient RPC(remote procedure call) and also messaging protocol with simplest structure you seen ever. Response and request header have same header structure! we suggest use syllab encoder to encode/decode payload data but it can work with other encoders too! Also we strongly suggest transfer it standalone above network protocols but it can transfer by including to other application protocol like HTTP!

## Goals
- minimum overhead to find service from server services
- minimum data exchange forces by protocol

## Not Goals
- Easy to read and write by human!

## Packet architecture
| bits        | data type               |
| ---         | :---:                   |
| 0 to 64     | Service ID or Error ID  |
| 64 to ...   | Payload                 |

### Service ID || Error ID
Read more about ServiceID [here](./Giti-Service.md) and ErrorID [here](./Giti-Error.md)

### Payload
Can be any encoded data in any format with any length! But we strongly suggest use [Syllab](./Syllab.md) for most efficient data encoder!

## Supported programming languages
It is so simple protocol that can easily encode and decode in any programming language! We implement it on some language like [C](), [Go](https://github.com/SabzCity/libgo/blob/master/srpc), [JavaScript]() and more in progress ...
