/* For license and copyright information please see the LEGAL file in the code repository */

package grp

import (
	"memar/protocol"

	gp "org/modules/group/protocol"
)

type StorageServices interface {
	Save(dm GroupRelated) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID gp.GroupUUID, relatedGroupID gp.GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID gp.GroupUUID, relatedGroupID gp.GroupUUID, vo protocol.VersionOffset) (dm GroupRelated, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_GroupIDs_BY_RelatedGroupID(relatedGroupID gp.GroupUUID, offset, limit uint64) (groupIDs []gp.GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_RelatedGroupIDs_BY_GroupID(groupID gp.GroupUUID, offset, limit uint64) (relatedGroupIDs []gp.GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
