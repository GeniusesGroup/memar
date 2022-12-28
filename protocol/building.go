/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type Building interface {
	BuildingID() [16]byte       // quiddity domain
	AreaID() [16]byte           // area domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type Building_StorageServices interface {
	Save(b Building) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(buildingID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(buildingID [16]byte, vo protocol.VersionOffset) (b Building, nv protocol.NumberOfVersion, err protocol.Error)

	FindByArea(areaID [16]byte, offset, limit uint64) (buildingIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	GetIDs(offset, limit uint64) (buildingIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type (
	Building_Service_Register_Request interface {
		BuildingID() [16]byte
		AreaID() [16]byte
	}
	Building_Service_Register_Response = protocol.NumberOfVersion
)

type (
	Building_Service_Count_Request interface {
		BuildingID() [16]byte
	}
	Building_Service_Count_Response = protocol.NumberOfVersion
)

type (
	Building_Service_Get_Request interface {
		BuildingID() [16]byte
		VersionOffset() protocol.VersionOffset
	}
	Building_Service_Get_Response1 = Building
	Building_Service_Get_Response2 = protocol.NumberOfVersion
)

type (
	Building_Service_GetIDs_Request interface {
		Offset() uint64
		Limit() uint64
	}
	Building_Service_GetIDs_Response interface {
		BuildingIDs() [][16]byte
		NumberOfVersion() protocol.NumberOfVersion
	}
)
