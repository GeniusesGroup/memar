/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// CommentGroup indicate the domain record data fields.
// each comment is immutable record and so use version mechanism to chain comments in a group.
type CommentGroup interface {
	GroupID() GroupUUID             //
	CommentID() CommentUUID         //
	UserID() UserUUID               //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CommentGroup_StorageServices interface {
	Save(cg CommentGroup) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID [16]byte, vo protocol.VersionOffset) (cg CommentGroup, nv protocol.NumberOfVersion, err protocol.Error)

	FindByComment(commentID [16]byte) (groupID [16]byte, err protocol.Error)
	FindByUser(groupID [16]byte, userID UserUUID, offset, limit uint64) (commentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	ListUserGroups(userID UserUUID, offset, limit uint64) (groupIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	// ListThreads(groupID [16]byte, offset, limit uint64) (commentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

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
