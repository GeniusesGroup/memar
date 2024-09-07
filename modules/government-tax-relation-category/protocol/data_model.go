/* For license and copyright information please see the LEGAL file in the code repository */

package trcp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	cp "org/modules/category/protocol"
	tp "org/modules/tax/protocol"
)

// DataModel indicate the domain record data fields.
// Tax Labels
// Setting tax labels allows you to perform the following actions:
// Define up to two tax labels and associate each of them with a specific tax rate
// Associate multiple tax rates with the same tax labels
// Associate a blank tax label with tax exempt items (considered non-value-added tax (VAT))
type DataModel interface {
	TaxID() tp.TaxUUID
	CategoryID() cp.CategoryUUID

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
