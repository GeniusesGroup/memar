/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// DiscountUsage indicate the domain record data fields.
type DiscountUsage interface {
	DiscountID() [16]byte       // product domain
	MaximumInvoice() uint64     //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type DiscountUsage_StorageServices interface {
	Save(du DiscountUsage) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (du DiscountUsage, nv protocol.NumberOfVersion, err protocol.Error)
}
