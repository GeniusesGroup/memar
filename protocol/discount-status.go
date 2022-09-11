/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// DiscountStatus indicate the domain record data fields.
type DiscountStatus interface {
	DiscountID() [16]byte       // discount domain
	Status() Discount_Status    //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type DiscountStatus_StorageServices interface {
	Save(ds DiscountStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (ds DiscountStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(status Discount_Status, offset, limit uint64) (discountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

type Discount_Status Quiddity_Status

const (
	Discount_Status_Expired = Discount_Status(Quiddity_Status_FreeFlag << iota)
	Discount_Status_End
)
