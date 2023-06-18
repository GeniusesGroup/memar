/* For license and copyright information please see the LEGAL file in the code repository */

package op

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields. each order is immutable record.
// use to register an order to e.g. exchange(an instruction to buy or sell) currencies
// A matching engine uses the orders book to determine which orders can be fully or partially executed.
type DataModel interface {
	OrderID() OrderUUID             //
	UserID() up.UserUUID            //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
