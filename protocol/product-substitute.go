/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProductSubstitute indicate the domain record data fields.
// or similar product
type ProductSubstitute interface {
	ProductID() [16]byte        // product domain
	Priority() uint64           // Substitute priority
	SubstituteID() [16]byte     // product domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductSubstitute_StorageServices interface {
	Save(ps ProductSubstitute) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (ps ProductSubstitute, nv protocol.NumberOfVersion, err protocol.Error)

	FindBySubstitute(substituteID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
