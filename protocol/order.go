/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type OrderUUID = protocol.UUID

// Order indicate the domain record data fields. each order is immutable record.
// use to register an order to e.g. exchange(an instruction to buy or sell) currencies
// A matching engine uses the orders book to determine which orders can be fully or partially executed.
type Order interface {
	OrderID() OrderUUID                     //
	UserID() protocol.UserID                // user domain
	Reference() [16]byte                    // Any ID that user can assign to track for any purpose. It can't be nil.
	ReferenceType() FinancialTransaction_RT //
	Time() protocol.Time                    // save time
	RequestID() UserRequestUUID             // user-request domain
}

type Order_StorageServices interface {
	Save(o Order) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(orderID [16]byte) (o Order, err protocol.Error)

	FindByUserID(userID [16]byte, offset, limit uint64) (orderIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
