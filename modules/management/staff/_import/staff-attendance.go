/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// StaffAttendance indicate the domain record data fields.
type StaffAttendance interface {
	StaffID() StaffUUID             //
	Type() StaffAttendance_Type     //
	AttendanceTime() protocol.Time  //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffAttendance_Type uint8

const (
	StaffAttendance_Type_Unset StaffAttendance_Type = iota
	StaffAttendance_Type_Enter
	StaffAttendance_Type_Exit
	StaffAttendance_Type_ManualEnter
	StaffAttendance_Type_ManualExit
	StaffAttendance_Type_Start
	StaffAttendance_Type_End
)
