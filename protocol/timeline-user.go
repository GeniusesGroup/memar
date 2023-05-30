/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// UserTimeline indicate the domain record data fields.
type UserTimeline interface {
	UserID() UserUUID               //
	GroupID() GroupUUID             // generate for group & comment domain
	Priority() uint64               //
	Status() UserTimeline_Status    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type UserTimeline_StorageServices interface {
	Save(ht UserTimeline) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID UserUUID, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID UserUUID, priority uint64, vo protocol.VersionOffset) (ht UserTimeline, nv protocol.NumberOfVersion, err protocol.Error)

	ListUser(groupID GroupUUID, offset, limit uint64) (userIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListGroup(userID UserUUID, offset, limit uint64) (groupIDs []GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListPriorities(userID UserUUID, groupID GroupUUID, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)

	// TODO:::
	// FilterByStatus(userID UserUUID, status UserTimeline_Status, offset, limit uint64) (groupIDs []GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type UserTimeline_Status Quiddity_Status

const (
// UserTimeline_Status_ = UserTimeline_Status(Quiddity_Status_FreeFlag << iota)
)
