/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"

	cp "org/modules/category/protocol"
	pp "org/modules/product/protocol"
	qrp "org/modules/quiddity-relation-type/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID
	Material_ProductID() pp.ProductUUID         // can be nil!
	Material_CategoryID() cp.CategoryUUID       // can be nil!
	RelationType() qrp.QuiddityRelationTypeUUID // Optional??
	MinQuantity() uint64
	BaseQuantity() uint64 // decimal >> 1.5 >> 1.2 >> 10 >> 0
	MaxQuantity() uint64
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
