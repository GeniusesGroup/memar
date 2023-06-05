/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// RoleAccess indicate the domain record data fields.
type RoleAccess interface {
	RoleID() RoleUUID                      //
	AccessControl() protocol.AccessControl //
	Time() protocol.Time                   // save time
	RequestID() urp.UserRequestUUID        //
}

type RoleAccess_StorageServices interface {
	Save(dm RoleAccess) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID RoleUUID, vo protocol.VersionOffset) (dm RoleAccess, nv protocol.NumberOfVersion, err protocol.Error)
}

// Get				GetRoleAccess
// GetRecursively	GetRoleAccessRecursively to get parent role access if the role has no access. bad service??
// Revoke			service to tell all node change role access control immediately
