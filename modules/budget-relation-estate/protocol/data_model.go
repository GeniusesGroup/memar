/* For license and copyright information please see the LEGAL file in the code repository */

package brep

import (
	"libgo/protocol"
	bp "org/modules/budget/protocol"
	eblp "org/modules/estate-building-location/protocol"
	ep "org/modules/estate/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID                       //
	EstateID() ep.EstateUUID                       //
	BuildingLocationID() eblp.BuildingLocationUUID //
	SaveTime() protocol.Time                       //
	RequestID() urp.UserRequestUUID                //
}
