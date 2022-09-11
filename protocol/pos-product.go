/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// PosServiceArea indicate the domain record data fields.
// Save shortcut to regular products to easily add to invoice
type PosProduct interface {
	PosID() [16]byte            // pos domain
	ProductID() [16]byte        // product domain.
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type PosProduct_StorageServices interface {
	Save(pp PosProduct) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(posID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(posID [16]byte, vo protocol.VersionOffset) (pp PosProduct, err protocol.Error)

	Delete(posID [16]byte, vo protocol.VersionOffset) (nv protocol.NumberOfVersion, err protocol.Error)
}
