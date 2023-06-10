/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductNumber indicate the domain record data fields.
type ProductNumber interface {
	ProductID() ProductUUID         //
	Minimum() uint64                // Minimum number of sale to serve the service e.g. cinema wouldn't play movie, ...
	Maximum() uint64                // Maximum number can be served to buyers e.g. cinema tickets, panic-room game, ...
	MaximumInvoiceByBuy() uint64    // Maximum buy e.g. hotel room, panic-room game, ... that must limit by buyer.
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductNumber_StorageServices interface {
	Save(dm ProductNumber) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (dm ProductNumber, nv protocol.NumberOfVersion, err protocol.Error)
}
