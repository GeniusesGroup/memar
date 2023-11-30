/* For license and copyright information please see the LEGAL file in the code repository */

package qsp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	qp "org/modules/quiddity/protocol"
)

// DataModel indicate the domain record data fields.
// or similar product
type DataModel interface {
	QuiddityID() qp.QuiddityUUID
	Priority() uint64
	SubstituteID() qp.QuiddityUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
