/* For license and copyright information please see the LEGAL file in the code repository */

package omp

import (
	"libgo/protocol"

	op "org/modules/order/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields. each order is immutable record.
type DataModel interface {
	OrderID() op.OrderUUID          //
	SideOrderID() op.OrderUUID      //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

