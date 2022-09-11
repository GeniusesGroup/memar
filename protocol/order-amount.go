/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// OrderAmount
type OrderAmount interface {
	OrderID() [16]byte          // order domain
	Amount() int64              // + || -		or Quantity
	Type() OrderAmount_Type     //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type OrderAmount_StorageServices interface {
	Save(oa OrderAmount) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(id [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(id [16]byte, vo protocol.VersionOffset) (oa OrderAmount, nv protocol.NumberOfVersion, err protocol.Error)
}

type OrderAmount_Type uint8

const (
	OrderAmount_Type_Unset   OrderAmount_Type = iota
	OrderAmount_Type_Regular                  // order-price rules
	OrderAmount_Type_Trade                    // order-trade rules
	// Whole order must be filled for matching deal or order must cancelled on timeout
	// If this flag absent, allow matching engine to deal part of order.
	// https://en.wikipedia.org/wiki/Immediate_or_cancel
	// https://en.wikipedia.org/wiki/All_or_none
	// https://en.wikipedia.org/wiki/Fill_or_kill
	OrderAmount_Type_MustFill
)
