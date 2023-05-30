/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// RoleLocation indicate the domain record data fields.
// Let staffs register enter and exit time by their mobiles in specific location.
type RoleLocation interface {
	RoleID() RoleUUID                         //
	BuildingLocationID() BuildingLocationUUID //
	Time() protocol.Time                      // save time
	RequestID() urp.UserRequestUUID           //
}

type RoleLocation_StorageServices interface {
	Save(rl RoleLocation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID RoleUUID, vo protocol.VersionOffset) (rl RoleLocation, nv protocol.NumberOfVersion, err protocol.Error)
}
