/* For license and copyright information please see the LEGAL file in the code repository */

package prp

import (
	"memar/protocol"

	pp "org/modules/product/protocol"
	rp "org/modules/role/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID
	RoleID() rp.RoleUUID
	Type() Type
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
