/* For license and copyright information please see the LEGAL file in the code repository */

package oap

import (
	"libgo/protocol"

	op "org/modules/order/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	OrderID() op.OrderUUID          //
	UserID() up.UserUUID            //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status uint8
