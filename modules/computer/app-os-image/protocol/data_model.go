/* For license and copyright information please see the LEGAL file in the code repository */

package oip

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
)

type DataModel interface {
	ImageID() ImageUUID
	ObjectID() protocol.UUID
	Status()

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
