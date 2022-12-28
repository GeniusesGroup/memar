/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// UserRelationStatus indicate the domain record data fields.
type UserRelationStatus interface {
	UserID() protocol.UserID     // user domain
	SideID() [16]byte            // user domain
	Status() UserRelation_Status //
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

type UserRelationStatus_StorageServices interface {
	Save(gs UserRelationStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID, sideID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID, sideID [16]byte, vo protocol.VersionOffset) (gs UserRelationStatus, nv protocol.NumberOfVersion, err protocol.Error)

	ListSides(userID [16]byte, offset, limit uint64) (sideIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListUsers(sideID [16]byte, offset, limit uint64) (userIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(userID [16]byte, status UserRelation_Status, offset, limit uint64) (sideIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

type UserRelation_Status Quiddity_Status

const (
	UserRelation_Status_Blocked = UserRelation_Status(Quiddity_Status_FreeFlag << iota)
	UserRelation_Status_Muted
)
