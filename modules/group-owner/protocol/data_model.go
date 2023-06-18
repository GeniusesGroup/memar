/* For license and copyright information please see the LEGAL file in the code repository */

package gop

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	GroupID() gp.GroupUUID          // or ChannelID. Use to store and retrieve comments in time order. It can be UUID, URL hash or any random id.
	OwnerUserID() up.UserUUID       //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
