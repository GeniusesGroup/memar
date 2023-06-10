/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductReserveQuantity indicate the domain record data fields.
type ProductReserveQuantity interface {
	ProductID() ProductUUID         //
	Quantity() uint64               // fix max reserve number
	Percent() uint64                // percent of the inventory
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductReserveQuantity_StorageServices interface {
	Save(dm ProductReserveQuantity) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (dm ProductReserveQuantity, nv protocol.NumberOfVersion, err protocol.Error)
}
