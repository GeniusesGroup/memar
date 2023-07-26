/* For license and copyright information please see the LEGAL file in the code repository */

package dp

import (
	"memar/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel or product-auction to reduce invoices price automatically by some rules know also as sales, ...
type DataModel interface {
	DiscountID() DiscountUUID
	Type() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

type Discount_GUI_Page_Services interface {
}
