# Codec Rules (`modules/computer/codec/rules/`)
Rules for codecs in this module — conditions work on format encode/decode is held to. The general Memar concept of Rule is defined in [`modules/process/rule/rule.md`](../../../process/rule/rule.md).

| Rule | Subject | What it is |
| --- | --- | --- |
| [Format Adjuncts](./format-adjuncts/format-adjuncts.md) | How types publish format encode/decode | Companion `<base>.codec.<format>.kh`; three seams; `codec-format-policy` manifest key; no mandatory format |
| [Format Module Provides Generator](./format-module-provides-generator/format-module-provides-generator.md) | What a format module must ship | Every format offers `Generate_Format_Adjunct` into `<base>.codec.<format>.kh` |
