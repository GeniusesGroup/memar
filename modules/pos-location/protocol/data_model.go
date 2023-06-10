/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// PosLocation indicate the domain record data fields.
type PosLocation interface {
	PosID() PosUUID                           //
	BuildingLocationID() BuildingLocationUUID //
	Time() protocol.Time                      // save time
	RequestID() urp.UserRequestUUID           //
}

type PosLocation_StorageServices interface {
	Save(dm PosLocation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(posID PosUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(posID PosUUID, vo protocol.VersionOffset) (dm PosLocation, err protocol.Error)

	FIND_PosIDs_BY_BuildingLocationID(BuildingLocationID BuildingLocationUUID, offset, limit uint64) (posIDs []PosUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
