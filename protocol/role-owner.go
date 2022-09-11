/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// RoleOwner indicate the domain record data fields.
type RoleOwner interface {
	RoleID() [16]byte           // role domain
	OwnerID() [16]byte          // department, group, user (delegate usage), ... domain
	OrgID() protocol.UserID     // belong to
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type RoleOwner_StorageServices interface {
	Save(ro RoleOwner) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID [16]byte, vo protocol.VersionOffset) (ro RoleOwner, nv protocol.NumberOfVersion, err protocol.Error)

	FindByOwner(ownerID [16]byte, offset, limit uint64) (roleIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	FindByOrg(orgID [16]byte, offset, limit uint64) (roleIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
