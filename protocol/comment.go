/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type CommentUUID = protocol.UUID

// Comment indicate the comment domain record data fields.
type Comment interface {
	CommentID() CommentUUID     //
	ReplyTo() CommentUUID       // Comment can be reply to other comment in the same group.
	UserID() protocol.UserID    // user domain
	Priority() uint64           //
	Type() Comment_Type         //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type Comment_StorageServices interface {
	Save(c Comment) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID [16]byte, vo protocol.VersionOffset) (c Comment, nv protocol.NumberOfVersion, err protocol.Error)

	FindByReplyTo(replyTo [16]byte, offset, limit uint64) (commentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type Comment_Type uint32

const (
	Comment_Type_Unset Comment_Type = 0
	Comment_Type_Text  Comment_Type = (1 << iota)
	Comment_Type_Voice
	Comment_Type_File

	Comment_Type_Call
	Comment_Type_Email

	Comment_Type_Image
	Comment_Type_Video
	Comment_Type_Album

	Comment_Type_Pin
	Comment_Type_Welcome
	Comment_Type_PhotoUpdated
	Comment_Type_NewConnection // made-friend, new-follower,

	Comment_Type_Map // location
	Comment_Type_Product

	Comment_Type_Thread  // Thread name will save in comment-text
	Comment_Type_Forward // Retweet, Share, ...
)

/*
	Business Services
*/

type (
	Comment_Service_Register_Request interface {
		GroupID() [16]byte
		ReplyTo() [16]byte
		UserID() protocol.UserID
		Type() Comment_Type
		Settings() Comment_Settings
	}
	Comment_Service_Register_Response interface {
		CommentID() CommentUUID
		NumberOfVersion() protocol.NumberOfVersion
	}
)

/*
	Errors
*/
