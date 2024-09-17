/* For license and copyright information please see the LEGAL file in the code repository */

package lvp

type Type uint8

const (
	LawVote_Type_Unset Type = iota
	LawVote_Type_Abstention
	LawVote_Type_Agree
	LawVote_Type_Disagree
)
