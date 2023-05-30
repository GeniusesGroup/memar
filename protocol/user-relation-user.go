/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// UserUserRelation indicate the domain record data fields.
type UserUserRelation interface {
	UserID() UserUUID               //
	SideID() UserUUID               //
	Relation() User_Relation        //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type UserUserRelation_StorageServices interface {
	Save(gs UserUserRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID, sideID UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID, sideID UserUUID, vo protocol.VersionOffset) (gs UserUserRelation, nv protocol.NumberOfVersion, err protocol.Error)

	ListSides(userID UserUUID, offset, limit uint64) (sideIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListUsers(sideID UserUUID, offset, limit uint64) (userIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

type User_Relation uint8

const (
	User_Relation_Unset User_Relation = iota
	User_Relation_1stFriendshipCycle
	User_Relation_2stFriendshipCycle
	User_Relation_3stFriendshipCycle
	User_Relation_4stFriendshipCycle
	User_Relation_5stFriendshipCycle
	User_Relation_6stFriendshipCycle

	// CommentFollow_Type_MakeFriend
	// CommentFollow_Type_Follow
)
