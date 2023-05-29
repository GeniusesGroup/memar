/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type StaffHire interface {
	UserID() UserUUID               //
	RoleID() RoleUUID               // role status
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffHire_StorageServices interface {
	Save(sh StaffHire) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID UserUUID, vo protocol.VersionOffset) (sh StaffHire, nv protocol.NumberOfVersion, err protocol.Error)

	FindByRoleID(roleID [16]byte, offset, limit uint64) (userIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}
