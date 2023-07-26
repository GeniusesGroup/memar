/* For license and copyright information please see the LEGAL file in the code repository */

package dap

import (
	"memar/protocol"

	dp "org/modules/discount/protocol"
	ep "org/modules/estate/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel is proper or appropriate location indicate specific area not specific location
// It's rule depend on products in invoices e.g. source or destination of taxi as a service(product).
type DataModel interface {
	DiscountID() dp.DiscountUUID
	EstateID() ep.EstateUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
