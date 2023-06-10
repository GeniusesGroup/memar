/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DiscountStatus indicate the domain record data fields.
type DiscountStatus interface {
	DiscountID() DiscountUUID       //
	Status() Discount_Status        //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountStatus_StorageServices interface {
	Save(dm DiscountStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm DiscountStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_DiscountIDs_BY_Status(status Discount_Status, offset, limit uint64) (discountIDs []DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

type Discount_Status Quiddity_Status

const (
	Discount_Status_Expired = Discount_Status(Quiddity_Status_FreeFlag << iota)
	Discount_Status_End
)
