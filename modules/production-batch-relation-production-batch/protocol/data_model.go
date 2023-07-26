/* For license and copyright information please see the LEGAL file in the code repository */

package pbrpbp

import (
	"memar/protocol"

	pbp "org/modules/production-batch/protocol"
)

// DataModel is the structure of production line.
type DataModel interface {
	ProductionBatchID() pbp.ProductionBatchUUID
	RelationID() pbp.ProductionBatchUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
