/* For license and copyright information please see the LEGAL file in the code repository */

package trp_p

import (
	aa_p "org/modules/app-audit/protocol"
	tax_p "org/modules/government-tax/protocol"
	product_p "org/modules/product/protocol"
	storage_p "org/modules/storage/protocol"
)

// ProductTax indicate the domain record data fields.
// Tax Labels
// Setting tax labels allows you to perform the following actions:
// Define up to two tax labels and associate each of them with a specific tax rate
// Associate multiple tax rates with the same tax labels
// Associate a blank tax label with tax exempt items (considered non-value-added tax (VAT))
type DataModel interface {
	tax_p.Field_TaxID
	product_p.Field_ProductID

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
