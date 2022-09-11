/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// RoleStatus indicate the domain record data fields.
type RoleStatus interface {
	RoleID() [16]byte           // role domain
	Status() Role_Status        //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type RoleStatus_StorageServices interface {
	Save(rs RoleStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID [16]byte, vo protocol.VersionOffset) (rs RoleStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(status Role_Status, offset, limit uint64) (roleIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type Role_Status Quiddity_Status

const (
	Role_Status_Recruit = Role_Status(Quiddity_Status_FreeFlag << iota) // Recruitment in progress
)
