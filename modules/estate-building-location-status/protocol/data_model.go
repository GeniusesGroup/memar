/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type BuildingLocationStatus interface {
	BuildingLocationID() [16]byte    // building-location domain
	Status() BuildingLocation_Status //
	Time() protocol.Time             // save time
	RequestID() urp.UserRequestUUID  //
}

type BuildingLocationStatus_StorageServices interface {
	Save(bs BuildingLocationStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(buildingLocationID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(buildingLocationID [16]byte, vo protocol.VersionOffset) (bs BuildingLocationStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(status BuildingLocation_Status, offset, limit uint64) (buildingLocationIDs [][16]byte, err protocol.Error)
	// protocol.EventTarget
}

type BuildingLocation_Status Quiddity_Status

const (
// BuildingLocation_Status_ = BuildingLocation_Status(Quiddity_Status_FreeFlag << iota)
)
