/* For license and copyright information please see the LEGAL file in the code repository */

package lrpp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	lotp "org/modules/lot/protocol"
	pbp "org/modules/production-batch/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	LotUUID() lotp.LotUUID
	BatchID() pbp.ProductionBatchUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
