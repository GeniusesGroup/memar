# IR words lexical model
## In one sentence
A pluggable [Lexical_Model](/modules/computer/lexer/protocol/lexical-model.kh) that cuts folded characters into word and phrase surfaces for inverted-index style Text use.

## Placement
Under the Text mirror: `modules-plugable/knowledge/text/lexical-models/ir-words/`. Kernel [Lexer](/modules/computer/lexer/lexer.md) owns decomposition; this folder owns the IR boundary choice ([Kernel neutrality](/modules/knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md)).

## Use
`Lex_Source` applies this model to a folded `CharacterRun`. Surfaces become [Labels](/modules/knowledge/label/label.md) through Label find/declare — that resolve step is not Lexer’s. Neural BPE/WordPiece is a different model, not this one.

Driven by task `20261103-T100549Z-14796`.
