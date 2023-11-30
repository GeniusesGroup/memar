/* For license and copyright information please see the LEGAL file in the code repository */

package osp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	op "org/modules/order/protocol"
)

// DataModel indicate the order-status domain record data fields.
type DataModel interface {
	OrderID() op.OrderUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
