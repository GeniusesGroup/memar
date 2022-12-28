/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// Order indicate the domain record data fields. each order is immutable record.
type OrderMatched interface {
	OrderID() OrderUUID         //
	SideOrderID() OrderUUID     //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type OrderMatched_StorageServices interface {
	Save(o OrderMatched) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(orderID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(orderID [16]byte, vo protocol.VersionOffset) (oe OrderMatched, nv protocol.NumberOfVersion, err protocol.Error)

	FindBySideID(sideOrderID [16]byte, offset, limit uint64) (orderIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
