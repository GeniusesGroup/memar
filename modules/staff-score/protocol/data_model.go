/* For license and copyright information please see the LEGAL file in the code repository */

package ssp

import (
	"libgo/protocol"

	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel or staff grade
type DataModel interface {
	StaffID() sp.StaffUUID          //
	Score() uint64                  //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
