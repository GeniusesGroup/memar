/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// CommentFollow indicate the domain record data fields.
type CommentFollow interface {
	CommentID() CommentUUID          // comment domain
	FollowedUserID() protocol.UserID // user domain. FollowedUserID
	Type() CommentFollow_Type        //
	Time() protocol.Time             // save time
	RequestID() UserRequestUUID      // user-request domain
}

type CommentFollow_Type uint8

// CommentFollow_Type_MakeFriend
// CommentFollow_Type_Follow
