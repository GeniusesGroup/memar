/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"

	pp "org/modules/product/protocol"
	prp "org/modules/production/protocol"
	qrp "org/modules/quiddity-relation-type/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductionID() prp.ProductionUUID
	ProductID() pp.ProductUUID
	MaterialID() pp.ProductUUID
	RelationType() qrp.QuiddityRelationTypeUUID // رویه پیتزا؟؟    Optional??
	MinQuantity() uint64
	BaseQuantity() uint64 // decimal >> 1.5 >> 1.2 >> 10 >> 0
	MaxQuantity() uint64
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
