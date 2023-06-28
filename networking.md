# Networking
All requirements in networking response with `frame` idea. Each network packet contains many frames in desire order that read by devices in a network to do some desire logic in each device, e.g. switching, routing, multiplexing, ...

## Frames
As describe in [sRPC](./sRPC.md) too, Each packet can carry many frames until respect network MTU. All frames have fixed first field name `Type` with `signed 8bit` length (Negative frame type reserved and use to extend types to int16 (or int64) length) that is same as [MediaTypeID](./media-type.md) but not use 64bit unsigned integer and standard here as a byte to minimize packet unnecessary overhead.

```go
type Frames struct {
    Type int16
}
```

## Frames Number
frames number will be register here in this table and must be respect by all:

| Num.  | Frame name   | Doc  |
| :---: | :---:        | :---:|
| 0     | Unset        | -------- |
| 1     | Asb          | [Protocol](./networking-osi_1-Asb.md) |
| 2     |              |                   |
| 3     |              |       |
| 4     |              |   |
| 5     |              |                       |
