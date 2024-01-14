/* For license and copyright information please see the LEGAL file in the code repository */

package trpp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	pp "org/modules/product/protocol"
	tp "org/modules/tax/protocol"
)

// ProductTax indicate the domain record data fields.
// Tax Labels
// Setting tax labels allows you to perform the following actions:
// Define up to two tax labels and associate each of them with a specific tax rate
// Associate multiple tax rates with the same tax labels
// Associate a blank tax label with tax exempt items (considered non-value-added tax (VAT))
type DataModel interface {
	TaxID() tp.TaxUUID
	ProductID() pp.ProductUUID

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
