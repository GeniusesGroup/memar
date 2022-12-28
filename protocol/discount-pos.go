/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// DiscountPOS indicate the domain record data fields.
type DiscountPOS interface {
	DiscountID() [16]byte       // discount domain
	PosID() [16]byte            // pos domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type DiscountPOS_StorageServices interface {
	Save(dp DiscountPOS) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (dp DiscountPOS, nv protocol.NumberOfVersion, err protocol.Error)

	FindByPOS(posID [16]byte, offset, limit uint64) (discountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
