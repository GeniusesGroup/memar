/* For license and copyright information please see the LEGAL file in the code repository */

package itvp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	ip "org/modules/invite/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InviteID() ip.InviteUUID        //
	Start() protocol.Time           //
	End() protocol.Time             //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
