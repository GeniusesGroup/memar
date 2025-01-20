/* For license and copyright information please see the LEGAL file in the code repository */

package psp

type Type uint8

const (
	Type_Unset           Type = 0
	Type_ChooseSeatByOrg Type = (1 << iota)
	Type_ChooseSeatByAttendanceTime
)
