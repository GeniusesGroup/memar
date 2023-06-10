/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// CommentGroup indicate the domain record data fields.
// each comment is immutable record and so use version mechanism to chain comments in a group.
type CommentGroup interface {
	GroupID() GroupUUID             //
	CommentID() CommentUUID         //
	UserID() up.UserUUID            //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CommentGroup_StorageServices interface {
	Save(dm CommentGroup) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID GroupUUID, vo protocol.VersionOffset) (dm CommentGroup, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_GroupIDs_BY_CommentID(commentID CommentUUID) (groupIDs []GroupUUID, err protocol.Error)
	FIND_GroupIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (groupIDs []GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_CommentIDs_By_GroupID(groupID GroupUUID, offset, limit uint64) (commentIDs []CommentUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

/*
	Business Services
*/

type (
	CommentGroup_Service_Register_Request interface {
		GroupID() GroupUUID
		CommentID() CommentUUID
	}
)

/*
	Errors
*/
