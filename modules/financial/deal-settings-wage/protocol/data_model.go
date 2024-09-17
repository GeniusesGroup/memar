/* For license and copyright information please see the LEGAL file in the code repository */

package osp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	oidp "org/modules/order-item-deal/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	OrderKind() oidp.Order_Kind
	PerMyriad()
	Amount()

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
