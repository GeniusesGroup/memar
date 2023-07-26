/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"

	op "org/modules/org/protocol"
	pp "org/modules/product/protocol"
	pbp "org/modules/production-batch/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductBatchID() ProductBatchUUID
	ProductionBatchID() pbp.ProductionBatchUUID
	ProductID() pp.ProductUUID
	OwnerID() op.OrgUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
