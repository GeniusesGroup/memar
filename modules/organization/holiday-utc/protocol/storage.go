/* For license and copyright information please see the LEGAL file in the code repository */

package ohup

import (
	"memar/protocol"
	"memar/time/utc"

	org "org/modules/org/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(orgID org.OrgUUID, week utc.WeekElapsed) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(orgID org.OrgUUID, week utc.WeekElapsed, vo protocol.VersionOffset) (dm DataModel, err protocol.Error)
}
