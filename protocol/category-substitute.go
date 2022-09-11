/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type CategorySubstitute interface {
	CategoryID() [16]byte       // category domain
	Priority() uint64           // Substitute priority
	SubstituteID() [16]byte     // category domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type CategorySubstitute_StorageServices interface {
	Save(cs CategorySubstitute) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(categoryID [16]byte, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(categoryID [16]byte, priority uint64, vo protocol.VersionOffset) (cs CategorySubstitute, nv protocol.NumberOfVersion, err protocol.Error)

	ListSubstitute(categoryID [16]byte, offset, limit uint64) (substituteIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListCategories(substituteID [16]byte, offset, limit uint64) (categoryIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListPriorities(substituteID, categoryID [16]byte, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)
}
