/* For license and copyright information please see the LEGAL file in the code repository */

package lttp

type Type uint64

const (
	Type_Unset   Type = 0
	Type_Content Type = (1 << iota)

	Type_FixedTypo

	// lexicon types
	Type_Text
	Type_Word
	Type_Term
	Type_Phrase

	// Anchor text — or link text or URI — is the visible, clickable text of a link.
	// It usually appears in a different color than the surrounding text and is often underlined.
	// Good link text tells the reader what to expect if they click on the link.
	// Email addresses > Jane.Doe@example.com || URLs > https://github.com/jdkato/prose
	Type_AnchorText
	// Mentions some topic e.g. #Victory
	Type_Hashtag
	// Mentions something e.g. tag a user > @omid
	Type_Mention
	// usually bot commands
	Type_Command
	// :-), >:(, o_0, etc.
	Type_Emoticon

	Type_Capitalization

	// TODO::: right or wrong?
	// When this word||phrase be in query it must answer with user location.
	// e.g. "Near Pizza Store"
	Type_Localization

	// https://en.wikipedia.org/wiki/Tag_(metadata)
	// A tag is generally a keyword or phrase that is assigned to a piece of information,
	// which helps to describe it and allows it to be found again.
	Type_Tag
	// Labels, conversely, serve a more explanatory or descriptive role,
	// offering direct information or instructions related to the item or data to which they are affixed.
	Type_Label

// PERSON           // People
// GPE              // geographical/political Entities (GPE
)

// ...
/*
	CC	conjunction, coordinating
	CD	cardinal number
	DT	determiner
	EX	existential there
	FW	foreign word
	IN	conjunction, subordinating or preposition
	JJ	adjective
	JJR	adjective, comparative
	JJS	adjective, superlative
	LS	list item marker
	MD	verb, modal auxiliary
	NN	noun, singular or mass
	NNP	noun, proper singular
	NNPS	noun, proper plural
	NNS	noun, plural
	PDT	predeterminer
	POS	possessive ending
	PRP	pronoun, personal
	PRP$	pronoun, possessive
	RB	adverb
	RBR	adverb, comparative
	RBS	adverb, superlative
	RP	adverb, particle
	SYM	symbol
	TO	infinitival to
	UH	interjection
	VB	verb, base form
	VBD	verb, past tense
	VBG	verb, gerund or present participle
	VBN	verb, past participle
	VBP	verb, non-3rd person singular present
	VBZ	verb, 3rd person singular present
	WDT	wh-determiner
	WP	wh-pronoun, personal
	WP$	wh-pronoun, possessive
	WRB	wh-adverb
*/
