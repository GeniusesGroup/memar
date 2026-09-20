/* For license and copyright information please see the LEGAL file in the code repository */

package od_p

const (
	Translation = iota
	Summarization

	// (news topic, ...)
	Labeling

	TextPrediction
	PunctuationDetection
	PunctuationCorrection
	SpellDetection
	SpellCorrection

	// The goal of lemmatization is to reduce a word to its root form, also called a lemma.
	// For example, the verb "running" would be identified as "run."
	Lemmatization

	OffenseDetection
)
