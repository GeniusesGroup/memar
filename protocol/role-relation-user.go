/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// RoleUserRelation indicate the domain record data fields.
type RoleUserRelation interface {
	RoleID() RoleUUID               //
	UserID() up.UserUUID            // user (delegate usage), ... domain
	Type() RoleUserRelation_Type    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type RoleUserRelation_StorageServices interface {
	Save(dm RoleUserRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID RoleUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID RoleUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm RoleUserRelation, nv protocol.NumberOfVersion, err protocol.Error)

	// FindByOwner(ownerID up.UserUUID, offset, limit uint64) (roleIDs []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_RoleIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (roleIDs []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_UserIDs_BY_RoleID(roleID RoleUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type RoleUserRelation_Type uint8

const (
	RoleUserRelation_Type_Unset RoleUserRelation_Type = iota
	RoleUserRelation_Type_RegisteredBy
	RoleUserRelation_Type_Issuer
	RoleUserRelation_Type_DelegateRole // Owner
)
