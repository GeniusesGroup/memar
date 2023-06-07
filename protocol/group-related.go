/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// GroupRelated indicate the domain record data fields.
type GroupRelated interface {
	GroupID() GroupUUID             //
	RelatedGroupID() GroupUUID      // Use to categorize and graph groups
	Status() GroupRelated_Status    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type GroupRelated_StorageServices interface {
	Save(dm GroupRelated) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID GroupUUID, relatedGroupID GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID GroupUUID, relatedGroupID GroupUUID, vo protocol.VersionOffset) (dm GroupRelated, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_GroupIDs_BY_RelatedGroupID(relatedGroupID GroupUUID, offset, limit uint64) (groupIDs []GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_RelatedGroupIDs_BY_GroupID(groupID GroupUUID, offset, limit uint64) (relatedGroupIDs []GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type GroupRelated_Status Quiddity_Status
