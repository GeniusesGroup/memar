/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductSeat indicate the domain record data fields.
type ProductSeat interface {
	ProductID() ProductUUID         //
	SeatCapacity() uint64           // max seat number
	Type() ProductSeat_Type         //
	MapID() ObjectUUID              // to show background and rows and seats. suggest use SVG format
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductSeat_StorageServices interface {
	Save(dm ProductSeat) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (dm ProductSeat, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_ProductIDs_BY_MapID(mapID ObjectUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FILTER_ProductIDs_BY_SeatType(t ProductSeat_Type, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProductSeat_Type uint8

const (
	ProductSeat_Type_Unset           ProductSeat_Type = 0
	ProductSeat_Type_ChooseSeatByOrg ProductSeat_Type = (1 << iota)
	ProductSeat_Type_ChooseSeatByAttendanceTime
)
