/* For license and copyright information please see the LEGAL file in the code repository */

package nap

import (
	"memar/protocol"

	np "org/modules/node/protocol"
)

type DataModel interface {
	UserID()
	NodeID() np.UUID
	NotificationChannel()
	DomainID() protocol.MediaTypeID
	LogLevel() protocol.LogLevel
	// TODO::: other condition

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// protocol.EventTarget
