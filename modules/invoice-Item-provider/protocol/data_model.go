/* For license and copyright information please see the LEGAL file in the code repository */

package iipp

import (
	"memar/protocol"

	ip "org/modules/invoice/protocol"
	pp "org/modules/product/protocol"
	sp "org/modules/staff/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID
	ProductID() pp.ProductUUID
	StaffID() sp.StaffUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
