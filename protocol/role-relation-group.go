/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// RoleGroupRelation indicate the domain record data fields.
type RoleGroupRelation interface {
	RoleID() RoleUUID               //
	GroupID() GroupUUID             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type RoleGroupRelation_StorageServices interface {
	Save(sf RoleGroupRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID RoleUUID, vo protocol.VersionOffset) (sf RoleGroupRelation, nv protocol.NumberOfVersion, err protocol.Error)

	FindByGroup(groupID GroupUUID, offset, limit uint64) (roleID []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}
