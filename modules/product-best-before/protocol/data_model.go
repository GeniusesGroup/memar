/* For license and copyright information please see the LEGAL file in the code repository */

package pbbp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
// https://en.wikipedia.org/wiki/Expiration_date
type DataModel interface {
	ProductID() pp.ProductUUID
	Duration() protocol.Duration // from production time

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
