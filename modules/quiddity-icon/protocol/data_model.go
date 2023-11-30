/* For license and copyright information please see the LEGAL file in the code repository */

package qip

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	op "org/modules/object/protocol"
	qp "org/modules/quiddity/protocol"
)

// DataModel indicate the domain record data fields.
// Icon or emoji use in many domains e.g. category, departments, ...
type DataModel interface {
	QuiddityID() qp.QuiddityUUID
	Icon() op.ObjectUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
