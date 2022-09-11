/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// OrderPrice indicate the invoice order-price record data fields.
// An order submitted without a specified price, and sequentially matched at the best available price in the market or in other words
// if user want to limit price, must fill order-price record otherwise market price will choose for the deals.
type OrderPrice interface {
	OrderID() [16]byte           // order domain
	Price() protocol.MoneyAmount // decimal, e.g. 1.258654, 0.987456487965
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

type OrderPrice_StorageServices interface {
	Save(op OrderPrice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(orderID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(orderID [16]byte, vo protocol.VersionOffset) (op OrderPrice, nv protocol.NumberOfVersion, err protocol.Error)
}
