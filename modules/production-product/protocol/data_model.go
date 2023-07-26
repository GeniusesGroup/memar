/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	"memar/protocol"

	prp "org/modules/product/protocol"
	pp "org/modules/production/protocol"
)

// DataModel is the structure of production line.
type DataModel interface {
	ProductionID() pp.ProductionUUID
	ProductID() prp.ProductUUID
	Type() Type
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
