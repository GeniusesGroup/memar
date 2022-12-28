/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// ProductSeat indicate the domain record data fields.
type ProductSeat interface {
	ProductID() [16]byte        // product domain
	SeatCapacity() uint64       // max seat number
	Type() ProductSeat_Type     //
	MapID() [16]byte            // object domain. to show background and rows and seats. suggest use SVG format
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductSeat_StorageServices interface {
	Save(ps ProductSeat) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (ps ProductSeat, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProductSeat_Type uint8

const (
	ProductSeat_Type_Unset           ProductSeat_Type = 0
	ProductSeat_Type_ChooseSeatByOrg ProductSeat_Type = (1 << iota)
	ProductSeat_Type_ChooseSeatByAttendanceTime
)
