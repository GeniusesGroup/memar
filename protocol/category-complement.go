/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type CategoryComplement interface {
	CategoryID() [16]byte       // category domain
	Priority() uint64           // Complement priority
	ComplementID() [16]byte     // category domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type CategoryComplement_StorageServices interface {
	Save(cs CategoryComplement) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(categoryID [16]byte, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(categoryID [16]byte, priority uint64, vo protocol.VersionOffset) (cs CategoryComplement, nv protocol.NumberOfVersion, err protocol.Error)

	ListCategories(complementID [16]byte, offset, limit uint64) (categoryIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListPriorities(complementID, categoryID [16]byte, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)
}

// services:
// ListSubstitute(categoryID [16]byte, offset, limit uint64) (complementIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
