/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type UserStatus interface {
	UserID() UserUUID               // Generated unique ID for the user
	OrgID() UserUUID                //
	Status() User_Status            //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type UserStatus_StorageServices interface {
	Save(us UserStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID UserUUID, vo protocol.VersionOffset) (us UserStatus, nv protocol.NumberOfVersion, err protocol.Error)

	GetIDs(offset, limit uint64) (userIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status UserOtherApp_Status, offset, limit uint64) (userIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	// FindByTime(day utc.DayElapsed, offset, limit uint64) (userIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type User_Status Quiddity_Status

const (
// User_Status_ = User_Status(Quiddity_Status_FreeFlag << iota)
)
