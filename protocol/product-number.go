/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// ProductNumber indicate the domain record data fields.
type ProductNumber interface {
	ProductID() [16]byte         // product domain
	Minimum() uint64             // Minimum number of sale to serve the service e.g. cinema wouldn't play movie, ...
	Maximum() uint64             // Maximum number can be served to buyers e.g. cinema tickets, panic-room game, ...
	MaximumInvoiceByBuy() uint64 // Maximum buy e.g. hotel room, panic-room game, ... that must limit by buyer.
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

type ProductNumber_StorageServices interface {
	Save(pa ProductNumber) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pa ProductNumber, nv protocol.NumberOfVersion, err protocol.Error)
}
