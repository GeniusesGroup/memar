/* For license and copyright information please see the LEGAL file in the code repository */

// use to register an order to e.g. exchange(an instruction to buy or sell) currencies
// A matching engine uses the orders book to determine which orders can be fully or partially executed.
//
// An DataModel submitted without a specified price, and sequentially matched at the best available price in the market or in other words
// if user want to limit price, must fill order-price record otherwise market price will choose for the deals.
package oidp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	op "org/modules/order/protocol"
)

// DataModel indicate the domain record data fields. each order is immutable record.
type DataModel interface {
	OrderID() op.OrderUUID
	SideType() SideType
	Kind() Order_Kind
	KindID() protocol.UUID // depend on kind A type
	Amount() int64         // + || -		or Quantity

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
