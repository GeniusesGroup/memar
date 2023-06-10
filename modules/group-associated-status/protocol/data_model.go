/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// GroupAssociatedStatus indicate the domain record data fields
type GroupAssociatedStatus interface {
	GroupID() GroupUUID             //
	UserID() up.UserUUID            //
	Status() GroupAssociated_Status //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type GroupAssociatedStatus_StorageServices interface {
	Save(dm GroupAssociatedStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID GroupUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID GroupUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm GroupAssociatedStatus, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_UserIDs_BY_GroupID_AND_Status(groupID GroupUUID, status GroupAssociated_Status, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type GroupAssociated_Status Quiddity_Status

const (
	GroupAssociated_Status_Joined = GroupAssociated_Status(Quiddity_Status_FreeFlag << iota)
	GroupAssociated_Status_Blocked
	GroupAssociated_Status_Muted

	GroupAssociated_Status_WaitToAcceptByAdmins
	GroupAssociated_Status_WaitToAcceptByUser
)
