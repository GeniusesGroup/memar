/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// GroupStatus indicate the domain record data fields.
type GroupStatus interface {
	GroupID() GroupUUID             // group-status domain
	Status() Group_Status           //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type GroupStatus_StorageServices interface {
	Save(gs GroupStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID [16]byte, vo protocol.VersionOffset) (gs GroupStatus, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status Picture_Status, offset, limit uint64) (groupIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type Group_Status Quiddity_Status

const (
// Group_Status_ = Group_Status(Quiddity_Status_FreeFlag << iota)
)
