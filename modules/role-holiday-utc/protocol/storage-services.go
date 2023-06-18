/* For license and copyright information please see the LEGAL file in the code repository */

package rhup

import (
	"libgo/protocol"
	"libgo/time/utc"

	rp "org/modules/role/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID rp.RoleUUID, week utc.WeekElapsed) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID rp.RoleUUID, week utc.WeekElapsed, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
