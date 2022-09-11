/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type StaffHire interface {
	UserID() protocol.UserID    // user domain
	RoleID() [16]byte           // role status
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type StaffHire_StorageServices interface {
	Save(sh StaffHire) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID [16]byte, vo protocol.VersionOffset) (sh StaffHire, nv protocol.NumberOfVersion, err protocol.Error)

	FindByRoleID(roleID [16]byte, offset, limit uint64) (userIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}
