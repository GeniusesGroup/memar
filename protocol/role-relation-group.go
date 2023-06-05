/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// RoleGroupRelation indicate the domain record data fields.
type RoleGroupRelation interface {
	RoleID() RoleUUID   //
	GroupID() GroupUUID //
	Status() Role_Group_Status
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type RoleGroupRelation_StorageServices interface {
	Save(f RoleGroupRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID RoleUUID, status Role_Group_Status) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID RoleUUID, status Role_Group_Status, vo protocol.VersionOffset) (f RoleGroupRelation, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_RoleIDs_BY_GroupID(groupID GroupUUID, offset, limit uint64) (roleIDs []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_GroupIDs_BY_RoleID(roleID RoleUUID, offset, limit uint64) (groupIDs []GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type Role_Group_Status Quiddity_Status
