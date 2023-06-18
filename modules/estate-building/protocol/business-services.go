/* For license and copyright information please see the LEGAL file in the code repository */

package ebp

import (
	"libgo/protocol"
)

type (
	BS_Register_Request interface {
		BuildingID() BuildingUUID
		AreaID() [16]byte
	}
	BS_Register_Response = protocol.NumberOfVersion
)

type (
	BS_Count_Request interface {
		BuildingID() [16]byte
	}
	BS_Count_Response = protocol.NumberOfVersion
)

type (
	BS_Get_Request interface {
		BuildingID() [16]byte
		VersionOffset() protocol.VersionOffset
	}
	BS_Get_Response1 = Building
	BS_Get_Response2 = protocol.NumberOfVersion
)

type (
	BS_GetIDs_Request interface {
		Offset() uint64
		Limit() uint64
	}
	BS_GetIDs_Response interface {
		BuildingIDs() [][16]byte
		NumberOfVersion() protocol.NumberOfVersion
	}
)
