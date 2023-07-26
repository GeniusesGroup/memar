/* For license and copyright information please see the LEGAL file in the code repository */

package odp

import (
	"memar/protocol"

	op "org/modules/order/protocol"
)

type DataModel interface {
	OrderID() op.OrderUUID
	Epoch() Epoch
	Duration() protocol.Duration // from Epoch()

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
