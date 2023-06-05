/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// RoleStaff indicate the domain record data fields.
type RoleStaff interface {
	RoleID() RoleUUID               //
	Minimum() int                   // Minimum number of employees for this job position
	Expected() int                  // Expected number of employees for this job position
	Maximum() int                   // Maximum number of employees for this job position
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type RoleStaff_StorageServices interface {
	Save(dm RoleStaff) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID RoleUUID, vo protocol.VersionOffset) (dm RoleStaff, nv protocol.NumberOfVersion, err protocol.Error)
}
