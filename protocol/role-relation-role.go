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
	Save(ro RoleRoleRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID RoleUUID, vo protocol.VersionOffset) (ro RoleRoleRelation, nv protocol.NumberOfVersion, err protocol.Error)

	FindByOther(otherID RoleUUID, offset, limit uint64) (roleIDs []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type RoleRoleRelation_Type uint8

const (
	RoleRoleRelation_Type_Unset RoleRoleRelation_Type = iota
	RoleRoleRelation_Type_SameLevel
	RoleRoleRelation_Type_UpperLevel
	RoleRoleRelation_Type_LowerLevel
)
