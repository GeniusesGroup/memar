/* For license and copyright information please see the LEGAL file in the code repository */

package jcd_p

type Field_Decision interface {
	Decision() Decision
}

// Decision or court decision
// Just accept specific decision type
type Decision uint64

const Decision_Unset Decision = 0
const (
	// a judgment disposing of the matter without a trial
	Decision_Dismissal Decision = (1 << iota)

	Decision_Invalidate

	// Guilty or accused
	Decision_Guilty

	// it will only be true if something else happens first
	Decision_Conditionally
)
