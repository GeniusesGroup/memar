/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// DiscountTimeValidity or LiveUntil indicate the domain record data fields.
type DiscountTimeValidity interface {
	DiscountID() [16]byte       // discount domain
	Start() protocol.Time       //
	End() protocol.Time         //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type DiscountTimeValidity_StorageServices interface {
	Save(dtv DiscountTimeValidity) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (dtv DiscountTimeValidity, nv protocol.NumberOfVersion, err protocol.Error)
}
