/* For license and copyright information please see the LEGAL file in the code repository */

package label

// Justice Case Relation User
const (
	Judge = iota

	// a body of citizens sworn to give a true verdict according to the evidence presented in a court of law
	// a committee appointed to judge a competition
	Jury

	// a person who brings an action in a court of law
	Plaintiff

	// a person or institution `against` whom an action is brought in a court of law;
	// the person being sued or accused (civil or criminal)
	Defendant
	// Suspect

	// the lawyer representing the defendant
	Lawyer

	// a lawyer who specializes in defending clients before a court of law
	TrialAttorney

	// a lawyer who pleads cases in court
	Counsellor

	// Many types of officer exist:
	// - bailiff: an officer of the court who is employed to execute writs and processes and make arrests etc.
	JudicialOfficer

	Witness
)
