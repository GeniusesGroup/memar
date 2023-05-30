/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// PosProvider indicate the domain record data fields.
// Provider or operator is to limit pos to specific staffs.
type PosProvider interface {
	PosID() PosUUID                 //
	RoleID() RoleUUID               //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
