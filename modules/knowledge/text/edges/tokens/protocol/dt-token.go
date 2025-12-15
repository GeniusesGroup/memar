/* For license and copyright information please see the LEGAL file in the code repository */

package tokens_p

// Token store detail about a word in the record to index
// Google name it as "Hit List"
// TODO::: Removing stop words?
type Token interface {
	Field_TokenType
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
