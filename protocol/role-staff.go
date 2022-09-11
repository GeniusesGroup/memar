/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// RoleStaff indicate the domain record data fields.
type RoleStaff interface {
	RoleID() [16]byte           // role domain
	Minimum() int               // Minimum number of employees for this job position
	Expected() int              // Expected number of employees for this job position
	Maximum() int               // Maximum number of employees for this job position
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type RoleStaff_StorageServices interface {
	Save(rs RoleStaff) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID [16]byte, vo protocol.VersionOffset) (rs RoleStaff, nv protocol.NumberOfVersion, err protocol.Error)
}
