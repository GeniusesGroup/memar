/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/math/per"
	"memar/protocol"

	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID //

	Materials() per.Myriad
	MaterialsCost() protocol.MoneyAmount
	Labor() per.Myriad
	LaborCost() protocol.MoneyAmount
	Investments() per.Myriad // Equipment
	InvestmentsCost() protocol.MoneyAmount
	TotalCost() protocol.MoneyAmount

	Markup() per.Myriad                    // the % added to the cost to determine the wholesale price
	WholesaleProfit() protocol.MoneyAmount // The amount of wholesale markup
	Margin() per.Myriad                    // the % of product price to determine the retail price
	RetailProfit() protocol.MoneyAmount    // The amount of retail margin

	Cost() protocol.MoneyAmount

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
