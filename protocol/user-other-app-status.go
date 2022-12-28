/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type UserOtherAppStatus interface {
	UserID() protocol.UserID     // user domain
	OrgID() protocol.UserID      // user domain
	Status() UserOtherApp_Status //
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

type UserOtherAppStatus_StorageServices interface {
	Save(uos UserOtherAppStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userOtherAppID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userOtherAppID [16]byte, vo protocol.VersionOffset) (uos UserOtherAppStatus, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status UserOtherApp_Status, offset, limit uint64) (userOtherAppIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type UserOtherApp_Status Quiddity_Status

const (
// UserOtherApp_Status_ UserOtherApp_Status = (Quiddity_Status_FreeFlag << iota)
)
