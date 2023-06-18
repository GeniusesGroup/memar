/* For license and copyright information please see the LEGAL file in the code repository */

package icp

import (
	"libgo/protocol"

	ip "org/modules/invite/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InviteID() ip.InviteUUID           //
	PermitUsageID() up.UserUUID     //
	ConsumerID() up.UserUUID        //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
