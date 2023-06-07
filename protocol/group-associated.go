/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// GroupAssociated indicate the domain record data fields
type GroupAssociated interface {
	GroupID() GroupUUID               //
	UserID() up.UserUUID              //
	JoinBy() up.UserUUID              //
	JoinWay() GroupAssociated_JoinWay //
	Time() protocol.Time              // save time
	RequestID() urp.UserRequestUUID   //
}

type GroupAssociated_StorageServices interface {
	Save(dm GroupAssociated) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID GroupUUID, vo protocol.VersionOffset) (dm GroupAssociated, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_UsersJoinWayIDs_BY_JoinWay(groupID GroupUUID, joinWay GroupAssociated_JoinWay, offset, limit uint64) (joinedBys []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_GroupIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (groupIDs []GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type GroupAssociated_JoinWay uint8

const (
	GroupAssociated_JoinWay_Unset GroupAssociated_JoinWay = iota
	GroupAssociated_JoinWay_Direct
	GroupAssociated_JoinWay_JoinLink
	GroupAssociated_JoinWay_Invite
)
