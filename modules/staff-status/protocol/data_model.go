/* For license and copyright information please see the LEGAL file in the code repository */

package ssp

import (
	"libgo/protocol"

	qsp "org/modules/quiddity-status/protocol"
	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	StaffID() sp.StaffUUID          //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
	Status_Hire = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_Fire
	Status_End // death, end of contract, ...
	// Status_Active   // Shift
	// Status_Inactive // Shift
)
