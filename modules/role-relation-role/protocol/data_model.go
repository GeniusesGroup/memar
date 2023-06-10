/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// RoleRoleRelation indicate the domain record data fields.
type RoleRoleRelation interface {
	RoleID() RoleUUID               //
	OtherID() RoleUUID              //
	Type() RoleRoleRelation_Type    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type RoleRoleRelation_StorageServices interface {
	Save(dm RoleRoleRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID RoleUUID, otherID RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID RoleUUID, otherID RoleUUID, vo protocol.VersionOffset) (dm RoleRoleRelation, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_OtherIDs_BY_RoleID(roleID RoleUUID, offset, limit uint64) (otherIDs []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_RoleIDs_BY_OtherID(otherID RoleUUID, offset, limit uint64) (roleIDs []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type RoleRoleRelation_Type uint8

const (
	RoleRoleRelation_Type_Unset RoleRoleRelation_Type = iota
	RoleRoleRelation_Type_SameLevel
	RoleRoleRelation_Type_UpperLevel
	RoleRoleRelation_Type_LowerLevel
)
