/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// OrderExchange use to exchange(an instruction to buy or sell) currencies
type OrderExchange interface {
	OrderID() [16]byte          // order domain
	SellAccountID() [16]byte    // financial-account domain
	BuyAccountID() [16]byte     // financial-account domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type OrderExchange_StorageServices interface {
	Save(oe OrderExchange) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(orderID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(orderID [16]byte, vo protocol.VersionOffset) (oe OrderExchange, nv protocol.NumberOfVersion, err protocol.Error)
}
