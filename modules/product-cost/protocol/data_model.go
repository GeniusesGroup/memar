/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID //

	Materials() protocol.PerMyriad
	MaterialsCost() protocol.MoneyAmount
	Labor() protocol.PerMyriad
	LaborCost() protocol.MoneyAmount
	Investments() protocol.PerMyriad
	InvestmentsCost() protocol.MoneyAmount
	TotalCost() protocol.MoneyAmount

	Markup() protocol.PerMyriad            // the % added to the cost to determine the wholesale price
	WholesaleProfit() protocol.MoneyAmount // The amount of wholesale markup
	Margin() protocol.PerMyriad            // the % of product price to determine the retail price
	RetailProfit() protocol.MoneyAmount    // The amount of retail margin

	Cost() protocol.MoneyAmount

	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
