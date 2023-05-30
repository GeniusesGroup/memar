/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// UserRelationStatus indicate the domain record data fields.
type UserRelationStatus interface {
	UserID() UserUUID               // user domain
	SideID() UserUUID               // user domain
	Status() UserRelation_Status    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type UserRelationStatus_StorageServices interface {
	Save(gs UserRelationStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID, sideID UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID, sideID UserUUID, vo protocol.VersionOffset) (gs UserRelationStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FindByStatus(userID UserUUID, status UserRelation_Status, offset, limit uint64) (sideIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

type UserRelation_Status Quiddity_Status

const (
	UserRelation_Status_Blocked = UserRelation_Status(Quiddity_Status_FreeFlag << iota)
	UserRelation_Status_Muted
)
