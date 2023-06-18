/* For license and copyright information please see the LEGAL file in the code repository */

package psp

import (
	"libgo/protocol"

	op "org/modules/object/protocol"
	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID      //
	SeatCapacity() uint64           // max seat number
	Type() Type                     //
	MapID() op.ObjectUUID           // to show background and rows and seats. suggest use SVG format
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset           Type = 0
	Type_ChooseSeatByOrg Type = (1 << iota)
	Type_ChooseSeatByAttendanceTime
)
