/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type CommentUUID = protocol.UUID

// Comment indicate the domain record data fields.
type Comment interface {
	CommentID() CommentUUID         //
	UserID() up.UserUUID            //
	Type() Comment_Type             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type Comment_StorageServices interface {
	Save(dm Comment) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID CommentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID CommentUUID, vo protocol.VersionOffset) (dm Comment, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_CommentIDs_BY_TYPE(t Comment_Type, offset, limit uint64) (commentIDs []CommentUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

type Comment_Type uint32

const (
	Comment_Type_Unset Comment_Type = 0
	Comment_Type_Text  Comment_Type = (1 << iota)
	Comment_Type_Voice
	Comment_Type_File

	Comment_Type_MultiParticipant
	Comment_Type_Email

	Comment_Type_Image
	Comment_Type_Video
	Comment_Type_Album

	Comment_Type_Pin
	Comment_Type_RelationToComment // Forward, Retweet, Share, ...

	// TODO:::
	Comment_Type_LogActivity_PrimaryKey_Single
	Comment_Type_LogActivity_PrimaryKey_Double
	Comment_Type_LogActivity_PrimaryKey_Triple
	Comment_Type_LogActivity_PrimaryKey_String
)

/*
	Business Services
*/

type (
	Comment_Service_Register_Request interface {
		GroupID() GroupUUID
		ReplyTo() [16]byte
		UserID() up.UserUUID
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

type Comment_GUI_Widget interface {
	Send()
}
