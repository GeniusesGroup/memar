/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// QuiddityComplement indicate the domain record data fields.
type QuiddityComplement interface {
	QuiddityID() QuiddityUUID   //
	Priority() uint64           // Complement priority
	ComplementID() QuiddityUUID //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type QuiddityComplement_StorageServices interface {
	Save(pc QuiddityComplement) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, priority uint64, vo protocol.VersionOffset) (pc QuiddityComplement, nv protocol.NumberOfVersion, err protocol.Error)

	ListQuiddities(complementID [16]byte, offset, limit uint64) (productIDs [16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListPriorities(complementID [16]byte, productID [16]byte, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)
}
