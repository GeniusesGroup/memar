/* For license and copyright information please see the LEGAL file in the code repository */

package gop

import (
	"memar/protocol"

	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	GroupID() gp.GroupUUID // or ChannelID. Use to store and retrieve comments in time order. It can be UUID, URL hash or any random id.
	OwnerUserID() up.UserUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
