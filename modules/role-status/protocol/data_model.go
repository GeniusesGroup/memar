/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// RoleStatus indicate the domain record data fields.
type RoleStatus interface {
	RoleID() RoleUUID               //
	Status() Role_Status            //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type RoleStatus_StorageServices interface {
	Save(dm RoleStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID RoleUUID, vo protocol.VersionOffset) (dm RoleStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_RoleIDs_BY_Status(status Role_Status, offset, limit uint64) (roleIDs []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

type Role_Status Quiddity_Status

const (
	Role_Status_Recruit = Role_Status(Quiddity_Status_FreeFlag << iota) // Recruitment in progress
)
