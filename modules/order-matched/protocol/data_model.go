/* For license and copyright information please see the LEGAL file in the code repository */

package omp

import (
	"memar/protocol"

	op "org/modules/order/protocol"
)

// DataModel indicate the domain record data fields. each order is immutable record.
type DataModel interface {
	OrderID() op.OrderUUID
	SideOrderID() op.OrderUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
