/* For license and copyright information please see the LEGAL file in the code repository */

package sip

import (
	"libgo/protocol"

	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
)

// TODO::: user-number??
type DataModel interface {
	StaffID() sp.StaffUUID          //
	ID() uint32                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
