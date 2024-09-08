/* For license and copyright information please see the LEGAL file in the code repository */

package pbp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	prp "org/modules/product/protocol"
	pp "org/modules/production/protocol"
)

// DataModel is the structure of production line.
type DataModel interface {
	ProductionBatchID() ProductionBatchUUID
	ProductID() prp.ProductUUID
	ProductionID() pp.ProductionUUID
	Number() uint64
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
