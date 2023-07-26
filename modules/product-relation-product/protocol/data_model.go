/* For license and copyright information please see the LEGAL file in the code repository */

package prpp

import (
	"memar/protocol"

	pp "org/modules/product/protocol"
	qrtp "org/modules/quiddity-relation-type/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID
	RelationID() pp.ProductUUID
	RelationType() qrtp.QuiddityRelationTypeUUID // رویه پیتزا؟؟    Optional??
	Quantity() uint64                            // decimal >> 1.5 >> 1.2 >> 10 >> 0
	MaxQuantity() uint64
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
