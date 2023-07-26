/* For license and copyright information please see the LEGAL file in the code repository */

package brep

import (
	"memar/protocol"

	bp "org/modules/budget/protocol"
	eblp "org/modules/estate-building-location/protocol"
	ep "org/modules/estate/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID
	EstateID() ep.EstateUUID
	BuildingLocationID() eblp.BuildingLocationUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
