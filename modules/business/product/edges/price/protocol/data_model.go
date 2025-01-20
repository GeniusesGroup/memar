/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	fcp "org/modules/financial-currency/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel can be register just by producer organization whom own the related quiddity
type DataModel interface {
	ProductID() pp.ProductUUID
	CurrencyID() fcp.FinancialCurrencyUUID
	Price() protocol.MoneyAmount // Basic Price, not payable price, in the currency

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
