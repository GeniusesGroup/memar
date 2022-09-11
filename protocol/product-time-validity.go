/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProductTimeValidity indicate the domain record data fields.
// flight departure and arrival time, concert start and end time, ...
type ProductTimeValidity interface {
	ProductID() [16]byte        // product domain
	Start() protocol.Time       //
	End() protocol.Time         //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductTimeValidity_StorageServices interface {
	Save(pt ProductTimeValidity) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pt ProductTimeValidity, nv protocol.NumberOfVersion, err protocol.Error)
}
