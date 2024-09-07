/* For license and copyright information please see the LEGAL file in the code repository */

package trd_p

import (
	aa_p "org/modules/app-audit/protocol"
	fm_p "org/modules/financial-money/protocol"
	tax_p "org/modules/government-tax/protocol"
	invoice_p "org/modules/invoice/protocol"
	product_p "org/modules/product/protocol"
	storage_p "org/modules/storage/protocol"
)

// DataModel indicate the domain record data fields. each order is immutable record.
type DataModel interface {
	invoice_p.Field_InvoiceID
	product_p.Field_ProductID
	tax_p.Field_TaxID

	fm_p.Field_Amount
	// VAT() fmp.MoneyAmount // Total VAT user pay to its country government

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
