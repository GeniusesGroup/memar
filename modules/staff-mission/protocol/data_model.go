/* For license and copyright information please see the LEGAL file in the code repository */

package smp

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	StaffID() sp.StaffUUID          //
	Day() utc.DayElapsed            //
	DayHours() earth.DayHours       //
	Type() Type                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_Meeting
	Type_Negotiation
	Type_Deal
	Type_Study
	// Type_
)
