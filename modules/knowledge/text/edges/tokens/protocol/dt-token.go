/* For license and copyright information please see the LEGAL file in the code repository */

package tokens_p

import (
	text_p "org/modules/knowledge/text/protocol"
)

// Token store detail about a word in the record to index
// Google name it as "Hit List"
// TODO::: Removing stop words?
type Token interface {
	// Text is token that store in one place to point it in any other text.
	text_p.Field_TextID

	WordOffsetInSentence() uint64 //  Position of the token in the sentence
	WordOffsetInText() uint64     //  Position of the word in the text
	OffsetInSentence() uint64     //  First word character position in the sentence
	OffsetInText() uint64         //  First word character position in the text

	// Words in a larger or bolder font are weighted higher than other words(tokens)
	Weight() uint64

	ScoreInSentence() uint64
	ScoreInText() uint64
	RankingScore() uint64
	// BackLinksNumbers() uint64 // citations numbers
}
