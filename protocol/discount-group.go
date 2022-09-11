/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// DiscountGroup indicate the domain record data fields.
type DiscountGroup interface {
	DiscountID() [16]byte       // discount domain
	GroupID() [16]byte          // group domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type DiscountGroup_StorageServices interface {
	Save(dg DiscountGroup) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (dg DiscountGroup, nv protocol.NumberOfVersion, err protocol.Error)

	FindByGroup(groupID [16]byte, offset, limit uint64) (discountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
