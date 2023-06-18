/* For license and copyright information please see the LEGAL file in the code repository */

package oidp

import (
	"libgo/protocol"

	op "org/modules/order/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields. each order is immutable record.
// use to register an order to e.g. exchange(an instruction to buy or sell) currencies
// A matching engine uses the orders book to determine which orders can be fully or partially executed.
//
// An DataModel submitted without a specified price, and sequentially matched at the best available price in the market or in other words
// if user want to limit price, must fill order-price record otherwise market price will choose for the deals.
type DataModel interface {
	OrderID() op.OrderUUID          //
	SideType() SideType             //
	Kind() Order_Kind               //
	KindID() [16]byte               // depend on kind A type
	Amount() int64                  // + || -		or Quantity
	Type() Type                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type SideType uint8

const (
	SideType_Unset SideType = iota
	SideType_Buy
	SideType_Sell
	// OrderItemDetail_SideType_...
)

// Use to send order to desire matching engine
type Order_Kind uint8

const (
	Order_Kind_Unset Order_Kind = 0
	Order_Kind_Money Order_Kind = (1 << iota) // usually Financial Exchange(an instruction to buy or sell) currencies, KindID==AccountID
	Order_Kind_Stock
	Order_Kind_Product
	// usually engine provide "NeedApprove" mechanism. https://en.wikipedia.org/wiki/Auction_theory
	Order_Kind_Auction
)

type Type uint8

const (
	OrderAmount_Type_Unset   Type = iota
	OrderAmount_Type_Regular      // order-price rules
	OrderAmount_Type_Trade        // order-trade rules
	// Whole order must be filled for matching deal or order must cancelled on timeout
	// If this flag absent, allow matching engine to deal part of order.
	// https://en.wikipedia.org/wiki/Immediate_or_cancel
	// https://en.wikipedia.org/wiki/All_or_none
	// https://en.wikipedia.org/wiki/Fill_or_kill
	OrderAmount_Type_MustFill
)
