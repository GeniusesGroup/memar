/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// OrderTrade indicate the invoice order-trade record data fields.
// can be zero to prevent sell on profit(cover order) or stopping loss
type OrderTrade interface {
	OrderID() [16]byte               // order domain
	Level() uint8                    // usually 3 level trade order
	HighPrice() protocol.MoneyAmount // SaveProfit	e.g. 45$ , -102$
	LowPrice() protocol.MoneyAmount  // StopLoss		e.g. 43$ , -95$
	Type() OrderTrade_Type           //
	Time() protocol.Time             // save time
	RequestID() UserRequestUUID      // user-request domain
}

type OrderTrade_StorageServices interface {
	Save(ot OrderTrade) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(orderID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(orderID [16]byte, vo protocol.VersionOffset) (ot OrderTrade, nv protocol.NumberOfVersion, err protocol.Error)
}

type OrderTrade_Type uint8

const (
	OrderTrade_Type_Unset OrderTrade_Type = iota
	// stop-loss orders guarantee execution
	OrderTrade_Type_StopLoss
	// stop-limit orders guarantee price
	OrderTrade_Type_StopLimit
)
