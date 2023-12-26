/* For license and copyright information please see the LEGAL file in the code repository */

package tp

type Type uint64

const (
	Type_Unset Type = 0
	Type_Text  Type = (1 << iota)
	Type_Word
	Type_Term
	Type_Phrase

	Type_Hashtag
	Type_Mention
	Type_Command // usually bot commands
)
