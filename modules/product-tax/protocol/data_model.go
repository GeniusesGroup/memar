/* For license and copyright information please see the LEGAL file in the code repository */

package ptp

import (
	"memar/math/per"
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	pp "org/modules/product/protocol"
	sp "org/modules/society/protocol"
)

// ProductTax indicate the domain record data fields.
// Tax Labels
// Setting tax labels allows you to perform the following actions:
// Define up to two tax labels and associate each of them with a specific tax rate
// Associate multiple tax rates with the same tax labels
// Associate a blank tax label with tax exempt items (considered non-value-added tax (VAT))
type DataModel interface {
	ProductID() pp.ProductUUID
	SocietyID() sp.SocietyUUID
	VAT() per.Myriad // VAT as Value-Added-Tax is bad name for a robbery

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
