/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type ContentContentRelated interface {
	ContentID() ContentUUID         //
	Priority() uint64               // substitute priority
	PriorityType() ContentTypeUUID  //
	RelatedID() ContentUUID         //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ContentContentRelated_StorageServices interface {
	Save(dm ContentContentRelated) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contentID ContentUUID, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contentID ContentUUID, priority uint64, vo protocol.VersionOffset) (dm ContentContentRelated, nv protocol.NumberOfVersion, err protocol.Error)
}
