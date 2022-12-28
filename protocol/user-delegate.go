/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// UserDelegate indicate the domain record data fields.
type UserDelegate interface {
	GivenUserID() protocol.UserID  // user domain
	GottenUserID() protocol.UserID // user domain
	OrgID() protocol.UserID        // user domain
	RoleID() [16]byte              // role domain
	Status() UserDelegate_Status   //
	Time() protocol.Time           // save time
	RequestID() UserRequestUUID    // user-request domain
}

type UserDelegate_StorageServices interface {
	Save(ud UserDelegate) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(givenUserID, gottenUserID, roleID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(givenUserID, gottenUserID, roleID [16]byte, vo protocol.VersionOffset) (ud UserDelegate, nv protocol.NumberOfVersion, err protocol.Error)

	ListOrgs(givenUserID [16]byte, offset, limit uint64) (orgIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListRoles(givenUserID, gottenUserID [16]byte, offset, limit uint64) (roles [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListUsers(roleID [16]byte, offset, limit uint64) (gottenUserIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListGottenDelegate(gottenUserID [16]byte, offset, limit uint64) (givenUserIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

type UserDelegate_Status Quiddity_Status

const (
// UserDelegate_Status_ = UserDelegate_Status(Quiddity_Status_FreeFlag << iota)
)

// Service: delegate user can delegate its role to other. blocked this service by default.
