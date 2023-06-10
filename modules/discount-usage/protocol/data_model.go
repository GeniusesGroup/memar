/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DiscountUsage indicate the domain record data fields.
type DiscountUsage interface {
	DiscountID() DiscountUUID       //
	MaximumInvoice() uint64         //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountUsage_StorageServices interface {
	Save(dm DiscountUsage) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm DiscountUsage, nv protocol.NumberOfVersion, err protocol.Error)
}
