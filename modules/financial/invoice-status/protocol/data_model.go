/* For license and copyright information please see the LEGAL file in the code repository */

package is_p

import (
	audit_p "org/modules/computer/audit/protocol"
	invoice_p "org/modules/financial/invoice/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	invoice_p.Field_InvoiceID
	Field_Status

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}
