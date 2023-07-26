/* For license and copyright information please see the LEGAL file in the code repository */

package cp

type Type uint32

const (
	Type_Unset Type = iota

	Type_FirstSide
	Type_SecondSide
	Type_ThirdSide
	Type_Witness
	Type_Arbitrator
	Type_Expert

	Type_Mass
	Type_Density

	Type_WeeklyRent
	Type_MonthlyRent

	Type_DueTo
)

// Service: fulfill the obligation
