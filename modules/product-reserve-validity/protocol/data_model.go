/* For license and copyright information please see the LEGAL file in the code repository */

package prvp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID
	Duration() protocol.Duration // from add to invoice time

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
