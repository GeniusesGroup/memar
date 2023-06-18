/* For license and copyright information please see the LEGAL file in the code repository */

package igp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	ip "org/modules/invite/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InviteID() ip.InviteUUID        //
	GroupID() gp.GroupUUID          //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
