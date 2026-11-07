---
Title: "Codec"
Labels: Draft
Start Date: 2026-11-06
ID: 498319
---
# Codec

## Abstract
A **codec** turns a value of one kind into a form and a form back into the value. It declares three things: an encode, which gives every value it is given a form; a decode, which gives back the value a form stands for; and a refusal, [`Codec_Error_NotDecodable`](errors/errors.kh), for a form it cannot decode. It says nothing about what the value means.

## What a codec is
- **A value that codes itself.** [`Codec`](protocol/codec.kh) is composed by a type whose own value writes itself into a buffer and reads itself back, as a protocol with one fixed encoding does (HTTP, Syllab). The form is part of the type.

## What every codec keeps
- **The value comes back.** Decoding the form a codec encoded gives back the value it was given.
- **A codec may read more forms than it writes.** It writes one form for each value and may decode other forms of the same value, such as an older form it once wrote; the form it writes is the one a reader is shown.
- **A form it does not decode is refused,** with `Codec_Error_NotDecodable`, and no value is guessed.
- **Nothing is kept.** The form is computed from the value and the value from the form.
