/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// GroupAssociatedRole indicate the domain record data fields.
type GroupAssociatedRole interface {
	GroupID() GroupUUID             //
	UserID() up.UserUUID            //
	RoleID() RoleUUID               //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type GroupAssociatedRole_StorageServices interface {
	Save(dm GroupAssociatedRole) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID GroupUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID GroupUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm GroupAssociatedRole, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_RoleIDs_BY_GroupID(groupID GroupUUID, userID up.UserUUID, offset, limit uint64) (roleIDs []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
