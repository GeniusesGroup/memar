/* For license and copyright information please see the LEGAL file in the code repository */

package gnp

import (
	"memar/protocol"

	gp "org/modules/group/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID gp.GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID gp.GroupUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_GroupIDs_BY_Name(name string, offset, limit uint64) (groupIDs []gp.GroupUUID, err protocol.Error)
	FILTER_GroupIDs_BY_Status(status Status, offset, limit uint64) (groupIDs []gp.GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
