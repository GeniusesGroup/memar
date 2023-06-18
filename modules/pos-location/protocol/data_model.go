/* For license and copyright information please see the LEGAL file in the code repository */

package plp

import (
	"libgo/protocol"

	eblp "org/modules/estate-building-location/protocol"
	pp "org/modules/pos/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	PosID() pp.PosUUID                             //
	BuildingLocationID() eblp.BuildingLocationUUID //
	SaveTime() protocol.Time                       //
	RequestID() urp.UserRequestUUID                //
}
