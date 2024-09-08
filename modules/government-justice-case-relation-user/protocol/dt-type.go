/* For license and copyright information please see the LEGAL file in the code repository */

package jcru_p

type Field_RelationType interface {
	RelationType() Type
}

type Type uint64

const Type_Unset Type = 0
const (
	Type_Judge Type = (1 << iota)

	// a body of citizens sworn to give a true verdict according to the evidence presented in a court of law
	// a committee appointed to judge a competition
	Type_Jury

	// a person who brings an action in a court of law
	Type_Plaintiff

	// a person or institution `against` whom an action is brought in a court of law;
	// the person being sued or accused (civil or criminal)
	Type_Defendant
	// Type_Suspect

	// the lawyer representing the defendant
	Type_Lawyer

	// a lawyer who specializes in defending clients before a court of law
	Type_TrialAttorney

	// a lawyer who pleads cases in court
	Type_Counsellor

	// Many types of officer exist:
	// - bailiff: an officer of the court who is employed to execute writs and processes and make arrests etc.
	Type_JudicialOfficer

	Type_Witness
)
