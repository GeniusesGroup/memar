/* For license and copyright information please see the LEGAL file in the code repository */

package pppp

import (
	"memar/protocol"

	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel store historically price with discount to show to users in price change chart.
type DataModel interface {
	ProductID() pp.ProductUUID
	// OrgID() org.OrgUUID
	Currency() uint64
	Price() protocol.MoneyAmount // Basic Price not payable price in the society currency

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
