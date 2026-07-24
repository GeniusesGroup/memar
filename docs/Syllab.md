# Syllab - Encoder
Syllab as most efficient data codec is a cross platform codec (data serialization/de-serialization system) library architected for maximum memory efficiency. It allows you to directly access serialized data without parsing/unpacking it first!
This codec architecture is very similar to memory management by programming languages that respect and influence by computer architecture that work in simplest way that can work just by bits (0&1)!

## Goals
- Simple but powerful structure
- Access serialized data without parsing/unpacking it first
- Small encode data size
- No memory(heap) allocation (or minimum in some programming language)
- Maximum coding (encode/decode) performance(time, resource and energy)
- Use in network and storage systems

## Not Goals
- Easy to coding (encode/decode) by humans
- Transfer data structure with data each time!
- Read data instantly by any program without related SDK
- Respect data model changed over times without any code changed! e.g. optional fields, serializing with missing fields for which defaults exist, ...
- Deprecating fields! Otherwise can achieve easily by not read from that field!!

## Architecture
Syllab encoder can almost encode/decode all data models (data types) in all programming language! It encode/decode data to two categories! Fixed and dynamically sized data! Fixed sized means peer know data always have same size like int8, int64, [16]byte, ...! These types of data encode by serialize in order from first byte of buffer in order they appear! In other side when peer don't know about size of data Syllab use heap like location in buffer in the end of fixed size data and point to address of it in simple but powerful manner! More complex dynamic size data types like maps split to some simple to encode||decode in these manners!

### Memory Blocks
A Syllab layout consists of the following types of memory blocks:
- Stack
- Heap

### Structures
You can see each language implementation that how complex type like slice, map, matrix ... encode/decode structure work! Any [hierarchical tree structure](https://en.wikipedia.org/wiki/Tree_(data_structure)) will inline in encode phase as flat structure!

#### Array (Fixed Size)
- **[01]byte** use to encode/decode any data up-to 008-bit size e.g. byte, boolean, int8, uint8, ...
- **[02]byte** use to encode/decode any data up-to 016-bit size e.g. int16, uint16, ...
- **[03]byte** use to encode/decode any data up-to 024-bit size e.g. int24, uint24, ...
- **[04]byte** use to encode/decode any data up-to 032-bit size e.g. int32, uint32, float32, rune, ...
- **[05]byte** use to encode/decode any data up-to 040-bit size e.g. int40, uint40, ...
- **[06]byte** use to encode/decode any data up-to 048-bit size e.g. int48, uint48, ...
- **[07]byte** use to encode/decode any data up-to 056-bit size e.g. int56, uint56, ...
- **[08]byte** use to encode/decode any data up-to 064-bit size e.g. int64, uint64, float64, int, uint, complex64, ...
- **[16]byte** use to encode/decode any data up-to 128-bit size e.g. int128, uint128, complex128, UUID, ...
- **[nn]byte** use to encode/decode any data up-to nn--bit size e.g. 32-byte keys, ...

#### Dynamically Size Array
Syllab convert dynamically size data to this simple structure of fixed size data! By this way our goals will be achieve specially access to any data in buffer without need to parse them! This type use for any types that don't have fix size like strings, files, ...
- 64-bit length in stack:
    - **first 32-bit of stack data** is address with uint32 type and size that point to location of data in whole buffer bytes! Due to improve performance and omit unnecessary plus calculation It count from start of buffer not start of heap part of buffer!
    - **last 32-bit of stack data** is length with uint32 type and size that indicate dynamically data size in bytes!
- n-bit in heap equal to array size carry array data
```go
// dynamicallyArray use for dynamically sized array data type
// that peer don't know about length of array before get data like []string, []uint8, ...
// It is just to show encoder||decoder structure in better way, we never use this type in any process!
type dynamicallyArray struct {
	arrayPointer uint32
	length       uint32
}
```

#### Hash Table - Map
We suggest below structure to decode/encode a hash table!
```go
// maps can encode and decode HashTable by two way
// - By two Array one for keys and one for values [key0, key1, ...] & [value0, value1, ...]
// - By continuous key and value that need dedicated encoder and decoder for each need!
// By now we just support first way in this package!
// It is just to show encoder structure in better way, we never use this type!
// https://github.com/golang/go/blob/master/src/runtime/map.go
type maps struct {
	keys   dynamicallyArray
	values dynamicallyArray
}
```

#### Tuple
Use an array(fixed or dynamically size) with desire length as number of the structure fields to encode/decode that carried values by below structure. Due to nature of some languages like Golang maybe peer don't accept some data types like tuple so we strongly don't suggest this tuple type! If you importunity ask this bad idea as software requirements like dynamic-typed languages (e.g. [JS with anything as object and properties](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)), Easily store and send any data by this trick but you must face truth and know that you get some performance penalty but still access data without need to parse them first!
```go
type tuple struct {
	arrayPointer uint32
	length       uint32
	dataType     uint8 // type of tuple field
}
```

### Size Limits
A Syllab buffer can't be larger than 2^128 and Non dynamically size array fields can be larger than 2^32

### Encoding example
Schema (Golang) :
```go
type test struct {
    meal   string
    say    string
    width  int32
    height int32
}
```
JSON :
```json
{ "meal": "Orange", "say": "hello", "width": 8000, "height": 7000 }
```
Syllab :
```syllab
stack:
  0000  00 00 00 20 00 00 00 06  00 00 00 26 00 00 00 05
  0010  00 00 00 00 00 00 1F 40  00 00 00 00 00 00 1B 58
heap:
  0020  4f 72 61 6e 67 65  68 65 6c 6c 6f
```

## Code Generations
It is very simple encoder base on code-generation for encode/decode process but also can marshal/un-marshal use by some runtime functions that we strongly don't suggest them!
Like our other RFCs, We suggest do logics in compile time not runtime to improve performance and efficiency. Syllab architecture is so simple that can easily implement by code generation not marshalling or un-marshalling in runtime!

## Supported Programming Languages
It is so simple protocol that can easily encode, decode & generate code in any programming language! We implement it on some language like [C](), [Go](https://github.com/GeniusesGroup/libgo/blob/master/syllab), [JavaScript]() and more in progress ...

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
