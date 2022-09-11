/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// RoleLocation indicate the domain record data fields.
// Let staffs register enter and exit time by their mobiles in specific location.
type RoleLocation interface {
	RoleID() [16]byte             // role domain
	BuildingLocationID() [16]byte // building-location domain
	Time() protocol.Time          // save time
	RequestID() UserRequestUUID   // user-request domain
}

type RoleLocation_StorageServices interface {
	Save(rl RoleLocation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID [16]byte, vo protocol.VersionOffset) (rl RoleLocation, nv protocol.NumberOfVersion, err protocol.Error)
}
