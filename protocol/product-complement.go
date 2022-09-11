/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProductComplement indicate the domain record data fields.
type ProductComplement interface {
	ProductID() [16]byte        // product domain
	Priority() uint64           // Complement priority
	ComplementID() [16]byte     // product domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductComplement_StorageServices interface {
	Save(pc ProductComplement) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, priority uint64, vo protocol.VersionOffset) (pc ProductComplement, nv protocol.NumberOfVersion, err protocol.Error)

	ListProducts(complementID [16]byte, offset, limit uint64) (productIDs [16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListPriorities(complementID [16]byte, productID [16]byte, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)
}
