/* For license and copyright information please see the LEGAL file in the code repository */

package pmup

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID
	Maximum() uint64 // Maximum time this service can be served to buyer

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
