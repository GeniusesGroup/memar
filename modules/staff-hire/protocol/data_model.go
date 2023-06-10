/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type StaffHire interface {
	UserID() up.UserUUID            //
	RoleID() RoleUUID               //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffHire_StorageServices interface {
	Save(dm StaffHire) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID, vo protocol.VersionOffset) (dm StaffHire, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_UserIDs_BY_RoleID(roleID RoleUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_RoleIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (roleIDs []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}
