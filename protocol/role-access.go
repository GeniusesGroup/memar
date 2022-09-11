/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// RoleAccess indicate the domain record data fields.
type RoleAccess interface {
	RoleID() [16]byte                      // role domain
	AccessControl() protocol.AccessControl //
	Time() protocol.Time                   // save time
	RequestID() UserRequestUUID            // user-request domain
}

type RoleAccess_StorageServices interface {
	Save(ra RoleAccess) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID [16]byte, vo protocol.VersionOffset) (ra RoleAccess, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

// Get				GetRoleAccess
// GetRecursively	GetRoleAccessRecursively to get parent role access if the role has no access. bad service??
// Revoke			service to tell all node change role access control immediately
