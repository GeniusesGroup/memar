/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DiscountTimeValidity or LiveUntil indicate the domain record data fields.
type DiscountTimeValidity interface {
	DiscountID() DiscountUUID       //
	Start() protocol.Time           //
	End() protocol.Time             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountTimeValidity_StorageServices interface {
	Save(dm DiscountTimeValidity) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm DiscountTimeValidity, nv protocol.NumberOfVersion, err protocol.Error)
}
