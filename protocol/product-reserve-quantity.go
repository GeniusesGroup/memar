/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// ProductReserveQuantity indicate the domain record data fields.
type ProductReserveQuantity interface {
	ProductID() [16]byte        // product domain
	Quantity() uint64           // fix max reserve number
	Percent() uint64            // percent of the inventory
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductReserveQuantity_StorageServices interface {
	Save(pr ProductReserveQuantity) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pr ProductReserveQuantity, nv protocol.NumberOfVersion, err protocol.Error)
}
