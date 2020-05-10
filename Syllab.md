# Syllab - Encoder
Syllab is data serialization/de-serialization system. It is very simple encoder base on code-generation for encode/decode process but also can marshal/un-marshal use by some runtime functions that we strongly don't suggest them!
This encoder respect and influence by computer architecture that work in simplest way that can work just by bits (0&1)!

## Goals
- Simple but powerful structure
- Access serialized data without parsing/unpacking it first
- Small encode data size
- No memory(heap) allocation (or minimum in some programming language)
- Maximum encode/decode performance
- Use in network and storage systems

## Not Goals
- Easy to encode/decode by humans
- Transfer data structure with data each time!
- Read data instantly by any program without related SDK
- Respect data model changed over times!

## Architecture
Syllab encoder can almost encode/decode all data models (data types) in all programming language! It encode/decode data to two categories! Fixed and dynamically sized data! Fixed sized means peer know data always have same size like int8, int64, [16]byte, ...! These types of data encode by serialize in order from first byte of buffer in order they appear! In other side when peer don't know about size of data Syllab use heap like location in buffer in the end of fixed size data and point to address of it in simple but powerful manner! More complex dynamic size data types like maps split to some simple to encode||decode in these manners!

Syllab convert dynamically size data to this simple structure of fixed size data! By this way our goals will be achieve specially access to any data in buffer without need to parse them!
- address with uint32 type and size that point to location of data in buffer bytes! It count from start of buffer not start of heap part of buffer!
- length with uint32 type and size that indicate dynamically data size in bytes!

You can see each language implementation that how complex type like slice, map, matrix ... encode/decode structure work! Any [hierarchical tree structure](https://en.wikipedia.org/wiki/Tree_(data_structure)) will inline in encode phase as flat structure!

## Supported Programming Languages
It is so simple protocol that can easily encode and decode in any programming language! We implement it on some language like [C](), [Go](https://github.com/SabzCity/libgo/blob/master/syllab), [JavaScript]() and more in progress ...

## Supported Code-Generations
It is so simple protocol that can easily implement in any code-generation apps! We implement it on some one like [Achaemenid](https://github.com/SabzCity/libgo/blob/master/Achaemenid-generator) and more in progress ...

## Inspired of
- https://github.com/alecthomas/go_serialization_benchmarks
- https://github.com/andyleap/gencode
- https://tools.ietf.org/html/rfc4506
- https://github.com/google/flatbuffers
- https://capnproto.org/
- https://en.wikipedia.org/wiki/Stack_(abstract_data_type)
- https://en.wikipedia.org/wiki/Memory_management#HEAP

## Syllab word meaning
Syllab is persian word that it seems came from syllable in Anglo-Norman variation of Old French sillabe, from Latin syllaba, from Koine Greek συλλαβή syllabḗ (Greek pronunciation: [sylːabɛ̌ː]). συλλαβή means "what is taken together", referring to letters that are taken together to make a single sound.
