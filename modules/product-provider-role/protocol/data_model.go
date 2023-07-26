/* For license and copyright information please see the LEGAL file in the code repository */

package pprp

import (
	"memar/protocol"

	pp "org/modules/product/protocol"
	rp "org/modules/role/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel or product operator is to supply a particular service.
// TODO::: role or group??
type DataModel interface {
	ProductID() pp.ProductUUID
	RoleID() rp.RoleUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
