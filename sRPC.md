# sRPC - Application Protocol
sRPC application protocol is most efficient RPC(remote procedure call) and also messaging protocol with simplest structure you seen ever. Response and request header have same header structure! we suggest use syllab encoder to encode/decode payload data but it can work with other encoders too! Also we strongly suggest transfer it standalone above network protocols but it can transfer by including to other application protocol like HTTP!

## Goals
- minimum overhead to find service from server services
- minimum data exchange

## Not Goals
- Easy to read and write by human!

## Packet architecture
| bits      | 32   |
| ---       | :---: |
| 1 to 32   |  ID <br/> request>>ServiceID <br/> response>>ErrorID - 0 means no error! |
| 33 to ... | Payload <br/> Can be any encode data |

## Supported programming languages
It is so simple protocol that can easily encode and decode in any programming language! We implement it on some language like [C](), [Go](https://github.com/SabzCity/libgo/blob/master/srpc), [JavaScript]() and more in progress ...
