/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// UserTimeline indicate the domain record data fields.
type UserTimeline interface {
	UserID() protocol.UserID     // user domain
	GroupID() GroupUUID          // generate for group & comment domain
	Priority() uint64            //
	Status() UserTimeline_Status //
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  //
}

type UserTimeline_StorageServices interface {
	Save(ht UserTimeline) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID [16]byte, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID [16]byte, priority uint64, vo protocol.VersionOffset) (ht UserTimeline, nv protocol.NumberOfVersion, err protocol.Error)

	ListUser(groupID [16]byte, offset, limit uint64) (userIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListGroup(userID [16]byte, offset, limit uint64) (groupIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListPriorities(userID, groupID [16]byte, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)

	// TODO:::
	// FilterByStatus(userID [16]byte, status UserTimeline_Status, offset, limit uint64) (groupIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type UserTimeline_Status Quiddity_Status

const (
// UserTimeline_Status_ = UserTimeline_Status(Quiddity_Status_FreeFlag << iota)
)
