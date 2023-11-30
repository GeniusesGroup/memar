/* For license and copyright information please see the LEGAL file in the code repository */

package qmp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	op "org/modules/object/protocol"
	qp "org/modules/quiddity/protocol"
)

type DataModel interface {
	QuiddityID() qp.QuiddityUUID
	Priority() uint64
	MediaID() op.ObjectUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
