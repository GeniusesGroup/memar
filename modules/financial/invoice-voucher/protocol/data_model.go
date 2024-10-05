/* For license and copyright information please see the LEGAL file in the code repository */

package iv_p

import (
	audit_p "org/modules/computer/audit/protocol"
	invoice_p "org/modules/financial/invoice/protocol"
	money_p "org/modules/financial/money/protocol"
	voucher_p "org/modules/financial/voucher/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
// This domain will let users redeem their vouchers and track vouchers rules.
type DataModel interface {
	invoice_p.Field_InvoiceID
	voucher_p.Field_VoucherID
	Discounted() money_p.Amount

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}
