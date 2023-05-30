/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// UserDelegate means transfer power to someone. power is role access in softwares.

// UserDelegate indicate the domain record data fields.
type UserDelegate interface {
	GivenUserID() UserUUID          //
	GottenUserID() UserUUID         //
	RoleID() RoleUUID               //
	Status() UserDelegate_Status    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type UserDelegate_StorageServices interface {
	Save(ud UserDelegate) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(givenUserID, gottenUserID UserUUID, roleID RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(givenUserID, gottenUserID UserUUID, roleID RoleUUID, vo protocol.VersionOffset) (ud UserDelegate, nv protocol.NumberOfVersion, err protocol.Error)

	ListRoles(givenUserID, gottenUserID UserUUID, offset, limit uint64) (roles []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListGottenUsers(roleID RoleUUID, offset, limit uint64) (gottenUserIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListGivenUsers(roleID RoleUUID, offset, limit uint64) (givenUserIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListGottenDelegateUsers(gottenUserID UserUUID, offset, limit uint64) (givenUserIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListGivenDelegateUsers(givenUserID UserUUID, offset, limit uint64) (gottenUserID []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type UserDelegate_Status Quiddity_Status

const (
// UserDelegate_Status_ = UserDelegate_Status(Quiddity_Status_FreeFlag << iota)
)

// Service: delegate user can delegate its role to other. blocked this service by default.
