/* For license and copyright information please see the LEGAL file in the code repository */

package ip

import (
	pos_p "org/modules/business/pos/protocol"
	audit_p "org/modules/computer/audit/protocol"
	invoice_p "org/modules/financial/invoice/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	invoice_p.Field_InvoiceID
	// InvoiceNumber() uint16      // TODO::: do we need auto increment number? Why not QR code?
	pos_p.Field_PosID

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}
