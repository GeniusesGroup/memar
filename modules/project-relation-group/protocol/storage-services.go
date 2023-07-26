/* For license and copyright information please see the LEGAL file in the code repository */

package prgp

import (
	"memar/protocol"

	gp "org/modules/group/protocol"
	pp "org/modules/project/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID pp.ProjectUUID, GroupID gp.GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID pp.ProjectUUID, GroupID gp.GroupUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_GroupIDs_BY_ProjectIDs(projectID pp.ProjectUUID, offset, limit uint64) (GroupIDs []gp.GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_ProjectIDs_BY_GroupID(GroupID gp.GroupUUID, offset, limit uint64) (projectIDs []pp.ProjectUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
