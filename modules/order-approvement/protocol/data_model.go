/* For license and copyright information please see the LEGAL file in the code repository */

package oap

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	op "org/modules/order/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	OrderID() op.OrderUUID
	UserID() up.UserUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
