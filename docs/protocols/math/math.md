---
Title: "Math"
Status: Draft
Start Date: 2026-09-29
ID: "497410"
---

# Math

## Abstract
This document is Memar's protocol for numeric magnitude and truth value: how fixed-width numbers are named in the tower, which values are not numeric widths even when their bits resemble one, and where implementations of that tower live in this repository. It is language-independent; a Khayyam realization names widths with `I`, `W`, and `R` prefixes and separates the one-valued truth capsule from the Boolean concept.

## Introduction

### Motivation
Reference corpora and host languages carry many numeric kinds — fixed widths, platform-chosen sizes, address-sized integers, bytes, runes, complex numbers — and conflating them produces wrong translations and contracts that name a capsule where an abstraction should stand. The tower and its exceptions must be stated once at the protocol layer so every realization and port shares the same mapping rules.

### Methodology
This Draft records positions already established in the corpus and in owner rulings carried from the memar-go port; it does not invent widths or concepts the declarations do not yet hold.

## Explanation

### The number tower
A numeric width is named by its number system and its width in bits: `I` for a signed integer, `W` for a whole (unsigned) integer, and `R` for a real number in floating point — for example `I16`, `W64`, and `R32` in the Khayyam realization under [`modules/math/`](../../../modules/math/). Each such name is a concrete width and therefore a capsule; the concept a width is an instance of — such as `Signed` — is an abstraction.

Truth values follow the same split: the capsule of one truth value (1 for true and 0 for false) is distinct from the concept of Boolean truth.

Four kinds of value are not numeric widths, even where their bits look like one:
- A complex number is an algebraic concept, not a width; no primitive capsule is a complex width.
- A width whose size the platform chooses, signed or unsigned, may be declared, and its declaration states that its size is the platform's and that it is error-prone. A translation from a language whose integer size is chosen by the platform does not map onto it silently.

### Realization membership
A declaration belongs under [`modules/math/`](../../../modules/math/) when its subject is a number or a truth value: a magnitude, an operation over magnitudes, a truth value, or the logic over truth values.

It does not belong there when its subject is something measured or encoded in numbers:
- a span or an instant of time — [`modules/time/`](../../../modules/time/README.md);
- a position among elements, which is a container's concept — [`modules/computer/adt/`](../../../modules/computer/adt/);
- an address in memory — [`modules/memory/address/`](../../../modules/memory/address/README.md);
- a character or an octet of an encoding — [`modules/codec/`](../../../modules/codec/).

Open questions on the tower, common numeric abstractions, and owner notes on library-implemented types are tracked in the paired [handoff](../math/math.handoff.md).
