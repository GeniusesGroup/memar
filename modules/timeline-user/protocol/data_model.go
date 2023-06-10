/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// UserTimeline indicate the domain record data fields.
type UserTimeline interface {
	UserID() up.UserUUID            //
	GroupID() GroupUUID             // generate for group & comment domain
	Priority() uint64               //
	Status() UserTimeline_Status    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type UserTimeline_StorageServices interface {
	Save(ht UserTimeline) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID, priority uint64, vo protocol.VersionOffset) (ht UserTimeline, nv protocol.NumberOfVersion, err protocol.Error)

	ListUser(groupID GroupUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListGroup(userID up.UserUUID, offset, limit uint64) (groupIDs []GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListPriorities(userID up.UserUUID, groupID GroupUUID, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)

	// TODO:::
	// FilterByStatus(userID up.UserUUID, status UserTimeline_Status, offset, limit uint64) (groupIDs []GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type UserTimeline_Status Quiddity_Status

const (
// UserTimeline_Status_ = UserTimeline_Status(Quiddity_Status_FreeFlag << iota)
)
