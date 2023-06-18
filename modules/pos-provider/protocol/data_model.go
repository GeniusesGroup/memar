/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	"libgo/protocol"

	pp "org/modules/pos/protocol"
	rp "org/modules/role/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// Provider or operator is to limit pos to specific staffs.
type DataModel interface {
	PosID() pp.PosUUID              //
	RoleID() rp.RoleUUID            //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
