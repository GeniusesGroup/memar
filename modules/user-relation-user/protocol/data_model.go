/* For license and copyright information please see the LEGAL file in the code repository */

package urup

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID            //
	SideID() up.UserUUID            //
	Relation() User_Relation        //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
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
