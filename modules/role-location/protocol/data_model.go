/* For license and copyright information please see the LEGAL file in the code repository */

package rlp

import (
	"libgo/protocol"

	eblp "org/modules/estate-building-location/protocol"
	qsp "org/modules/quiddity-status/protocol"
	rp "org/modules/role/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// Let staffs register enter and exit time by their mobiles in specific location.
type DataModel interface {
	RoleID() rp.RoleUUID                           //
	BuildingLocationID() eblp.BuildingLocationUUID //
	Status() Status
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status
