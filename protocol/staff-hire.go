/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type StaffHire interface {
	UserID() up.UserUUID            //
	RoleID() RoleUUID               // role status
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffHire_StorageServices interface {
	Save(f StaffHire) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID, vo protocol.VersionOffset) (f StaffHire, nv protocol.NumberOfVersion, err protocol.Error)

	FindByRoleID(roleID RoleUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}
