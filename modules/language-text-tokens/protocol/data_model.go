/* For license and copyright information please see the LEGAL file in the code repository */

package lttp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	amp "org/modules/app-module/protocol"
	ltp "org/modules/language-text/protocol"
	lwp "org/modules/language-word/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TextID() ltp.TextUUID     // MUST be Type_Content
	Analyzer() amp.ModuleUUID // module+version
	Tokens() []Token

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// Token store detail about a word in the record to index
// Google name it as "Hit List"
// TODO::: Removing stop words?
type Token interface {
	WordID() lwp.WordUUID
	Type() Type
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
