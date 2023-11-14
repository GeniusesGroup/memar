/* For license and copyright information please see the LEGAL file in the code repository */

package osp

import (
	"memar/protocol"

	dp "org/modules/deal/protocol"
)

// DataModel indicate the order-status domain record data fields.
type DataModel interface {
	DealID() dp.DealUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
