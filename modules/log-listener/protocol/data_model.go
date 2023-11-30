/* For license and copyright information please see the LEGAL file in the code repository */

package nap

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	np "org/modules/node/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID
	NodeID() np.NodeUUID
	NotificationChannel()
	DomainID() protocol.MediaTypeID
	LogLevel() protocol.LogLevel
	// TODO::: other condition

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// protocol.EventTarget
