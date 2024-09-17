/* For license and copyright information please see the LEGAL file in the code repository */

package orp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	op "org/modules/order/protocol"
)

// DataModel indicate the domain record data fields. each order is immutable record.
type DataModel interface {
	OrderID() op.OrderUUID
	Reference() [16]byte // Any ID that user can assign to track for any purpose. It can't be nil.
	ReferenceType() uint8

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
