/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// Order indicate the domain record data fields. each order is immutable record.
// use to register an order to e.g. exchange(an instruction to buy or sell) currencies
// A matching engine uses the orders book to determine which orders can be fully or partially executed.
type Order interface {
	OrderID() [16]byte          //
	UserID() protocol.UserID    // user domain
	Kind() Order_Kind           //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type Order_StorageServices interface {
	Save(o Order) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(orderID [16]byte) (o Order, err protocol.Error)

	FindByUserID(userID [16]byte, offset, limit uint64) (orderIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

// Use to send order to desire matching engine
type Order_Kind uint8

const (
	Order_Kind_Unset Order_Kind = 0
	Order_Kind_Exchange
	Order_Kind_Stock
	Order_Kind_Product
	// usually engine provide "NeedAprove" mechanism. https://en.wikipedia.org/wiki/Auction_theory
	Order_Kind_Auction
)
