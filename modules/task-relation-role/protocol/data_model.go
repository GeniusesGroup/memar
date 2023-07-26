/* For license and copyright information please see the LEGAL file in the code repository */

/*
- Some product as material need or pend on other production, .e.g. car needs engine, ...
*/
package prrp

import (
	"memar/protocol"

	pp "org/modules/production/protocol"
	rp "org/modules/role/protocol"
)

type DataModel interface {
	ProductionID() pp.ProductionUUID
	Role() rp.RoleUUID
	Type() Type
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
