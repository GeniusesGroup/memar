/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DiscountPOS indicate the domain record data fields.
type DiscountPOS interface {
	DiscountID() DiscountUUID       //
	PosID() PosUUID                 //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountPOS_StorageServices interface {
	Save(dm DiscountPOS) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm DiscountPOS, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_DiscountIDs_BY_PosID(posID PosUUID, offset, limit uint64) (discountIDs []DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
