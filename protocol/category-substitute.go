/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type CategorySubstitute interface {
	CategoryID() CategoryUUID       //
	Priority() uint64               // Substitute priority
	SubstituteID() CategoryUUID     //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CategorySubstitute_StorageServices interface {
	Save(cs CategorySubstitute) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(categoryID [16]byte, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(categoryID [16]byte, priority uint64, vo protocol.VersionOffset) (cs CategorySubstitute, nv protocol.NumberOfVersion, err protocol.Error)

	ListSubstitute(categoryID [16]byte, offset, limit uint64) (substituteIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListCategories(substituteID [16]byte, offset, limit uint64) (categoryIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListPriorities(substituteID, categoryID [16]byte, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)
}
