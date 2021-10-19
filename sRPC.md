# sRPC - Application Protocol
sRPC (Syllab Remote Procedure Call) is a RPC(remote procedure call) protocol. It is develope to use by [GP](./Giti-Network.md) protocol, But it can also use to be a messaging protocol among with other protocol that implement fundamental part of streaming requirements like HTTP, ...

## Goals
- Minimum overhead to find service from server services
- Minimum data exchange forces by protocol

## Not Goals
- Easy to understand by human

## Rules
### Service ID
- It is on request and use to route service and call the handler!
- Read more about ServiceID [here](./Service.md)
- Transfer base on the protocol e.g. http-uri: "/apis?{{.ServiceID}}"

### Error ID
- It is on response packet and use to show if calling service occur an error!
- Read more about ErrorID [here](./Error.md)
- Transfer base on the protocol e.g. http-header: "Error-ID: {{.ErrorID}}"

### Payload (Request or Response)
Payload with any length that service force to accept it on its specs is [Syllab](./Syllab.md) codec.   
*Just for your information, payload can be other codecs like json too but it is not standard and not suggest from us.*

## Supported programming languages
It is so simple protocol that can easily encode and decode in any programming language! We implement it on some language like [C](), [Go](https://github.com/GeniusesGroup/libgo/blob/master/srpc), [JavaScript](https://github.com/GeniusesGroup/libjs/blob/master/polyfills/http.js) and more in progress ...
