/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// GroupStatus indicate the domain record data fields.
type GroupStatus interface {
	GroupID() GroupUUID
	UserID() up.UserUUID            //
	Status() Group_Status           //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type GroupStatus_StorageServices interface {
	Save(dm GroupStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID GroupUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID GroupUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm GroupStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_GroupIDs_BY_Status(status Group_Status, offset, limit uint64) (groupIDs []GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type Group_Status Quiddity_Status

const (
// Group_Status_ = Group_Status(Quiddity_Status_FreeFlag << iota)
)
