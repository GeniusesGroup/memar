# Character Codec
This structure like UTF based encode system but with some improvement to reduce waste of bits. Like UTF-8, This encode system is designed in a such way that all ASCII characters use the same byte representation. 

## Encoding
Always first bit of first byte must be "0" and First bit of second and further byte must be "1".

Each script get a byte to encode their characters. English as ASCII always start bit with 0 but other scripts like Persian always start bit with 1. If we have 1 effective byte, it means ASCII characters exist. If we have 2 effective bytes, it means first one is not ASCII character code and it use to detect script ID. and 2nd byte is script character. If we have 3 effective bytes, it means 1th&2nd is not character code and it use to detect script ID. and 3rd byte is script character. And this rule can go for ever, But we think we don't need more than 4 byte that can encode 2,097,152 script and 266,338,304 characters.

| Effective	| Byte 1		| Byte 2		| Byte 3		| Byte 4		| ...   |
| :---:     | :---:         | :---:         | :---:         | :---:         | :---: |
| byte		| (int8)		| (int8)		| (int8)		| (int8)		| ...   |
| 1			| 0xxxxxxx      | 10000000      | 10000000      | 10000000      | ...   |
| 2			| 0sssssss      | 1xxxxxxx      | 10000000      | 10000000      | ...   |
| 3			| 0sssssss      | 1sssssss      | 1xxxxxxx      | 10000000      | ...   |
| 4			| 0sssssss      | 1sssssss      | 1sssssss      | 1xxxxxxx      | ...   |
| ...		| ...           | ...			| ...			| ...			| ...   |

## Compression
- ["10000000" bit || "0x80" hex || "128" byte(uint8) || "-0" int8] can be omitted any where in compressed text.

## Goals
- **Backward compatibility**: Backward compatibility with ASCII and the enormous amount of software designed to process ASCII-encoded text was the main driving force behind the design 
- **Prefix code**: Reading from a stream can instantaneously decode each individual fully received sequence, without first having to wait for either the first byte of a next sequence or an end-of-stream indication.
- **The length of multi-byte sequences** is easily determined by humans. We believe 4 effective bytes is enough for encoding more than 266,338,304 characters but this encode system can use for more than 4 bytes and can increase to n bytes.
- [**Self Synchronization**](https://en.wikipedia.org/wiki/Self-synchronizing_code): It can be self-synchronizing on both compress or uncompressed style. The leading bytes and the continuation bytes do not share values (continuation bytes start with the bits 1 while single bytes start with 0). This means a search will not accidentally find the sequence for one character starting in the middle of another character. It also means the start of a character can be found from a random position by backing up at most 3 bytes to find the leading byte. An incorrect character will not be decoded if a stream starts mid-sequence, and a shorter sequence will never appear inside a longer one.
- **Most efficient process usage** to encode using simple bitwise operations. It does not require slower mathematical operations such as multiplication or division (unlike Shift JIS, GB 2312 and other encodings).
- **Most efficient memory usage** in almost same level with a multi-byte encoding designed for a specific script. East Asian legacy encodings generally used two bytes per character and it will cost here two byte too.

## Non Goals (Non Considering that can be treated as disadvantages)
- **An incorrect character** can be decoded wrongly in compress form, if a stream ends mid-sequence.

## Still considering
- We have very strong argue that some ASCII codes like control one is waste of first byte and we can reuse them for other characters.
- **Numbering characters**: Do we need each human language introduce number character? It is GUI problem not character codec problem to display numbers in desire language format base on the number context.

## Others
- [ASCII](https://en.wikipedia.org/wiki/ASCII)
- [UTF-8](https://en.wikipedia.org/wiki/UTF-8)
