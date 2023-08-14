/* For license and copyright information please see the LEGAL file in the code repository */

package pdp

import (
	"memar/protocol"

	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID
	Epoch() Epoch
	Duration() protocol.Duration // from first use

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
