/* For license and copyright information please see the LEGAL file in the code repository */

package rrop

import (
	"memar/protocol"

	org "org/modules/org/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(organizationID org.OrgUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(organizationID org.OrgUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
