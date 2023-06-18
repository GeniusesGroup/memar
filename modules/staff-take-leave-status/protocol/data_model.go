/* For license and copyright information please see the LEGAL file in the code repository */

package stlsp

import (
	"libgo/protocol"
	"libgo/time/utc"

	qsp "org/modules/quiddity-status/protocol"
	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	StaffID() sp.StaffUUID          //
	Day() utc.DayElapsed            //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
	Status_NeedAlternate = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_NeedAlternateApprove
	Status_AlternateApprove
	Status_NeedManagerApprove
	Status_ManagerApprove
)
