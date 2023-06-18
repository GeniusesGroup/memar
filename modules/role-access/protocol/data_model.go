/* For license and copyright information please see the LEGAL file in the code repository */

package rap

import (
	"libgo/protocol"

	rp "org/modules/role/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	RoleID() rp.RoleUUID                   //
	AccessControl() protocol.AccessControl //
	SaveTime() protocol.Time               //
	RequestID() urp.UserRequestUUID        //
}
