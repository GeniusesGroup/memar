/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// UserDelegate means transfer power to someone. power is role access in softwares.

// UserDelegate indicate the domain record data fields.
type UserDelegate interface {
	GivenUserID() protocol.UserID   // user domain
	GottenUserID() protocol.UserID  // user domain
	RoleID() RoleUUID               //
	Status() UserDelegate_Status    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID // user-request domain
}

type UserDelegate_StorageServices interface {
	Save(ud UserDelegate) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(givenUserID, gottenUserID [16]byte, roleID RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(givenUserID, gottenUserID [16]byte, roleID RoleUUID, vo protocol.VersionOffset) (ud UserDelegate, nv protocol.NumberOfVersion, err protocol.Error)

	ListRoles(givenUserID, gottenUserID [16]byte, offset, limit uint64) (roles [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListGottenUsers(roleID [16]byte, offset, limit uint64) (gottenUserIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListGivenUsers(roleID [16]byte, offset, limit uint64) (givenUserIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListGottenDelegateUsers(gottenUserID [16]byte, offset, limit uint64) (givenUserIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListGivenDelegateUsers(givenUserID [16]byte, offset, limit uint64) (gottenUserID [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type UserDelegate_Status Quiddity_Status

const (
// UserDelegate_Status_ = UserDelegate_Status(Quiddity_Status_FreeFlag << iota)
)

// Service: delegate user can delegate its role to other. blocked this service by default.
