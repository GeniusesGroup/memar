/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// QuidditySubstitute indicate the domain record data fields.
// or similar product
type QuidditySubstitute interface {
	QuiddityID() QuiddityUUID   //
	Priority() uint64           // Substitute priority
	SubstituteID() QuiddityUUID //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type QuidditySubstitute_StorageServices interface {
	Save(ps QuidditySubstitute) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (ps QuidditySubstitute, nv protocol.NumberOfVersion, err protocol.Error)

	FindBySubstitute(substituteID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
