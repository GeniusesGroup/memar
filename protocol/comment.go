/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type CommentUUID = protocol.UUID

// Comment indicate the domain record data fields.
type Comment interface {
	CommentID() CommentUUID         //
	UserID() UserUUID               //
	Type() Comment_Type             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type Comment_StorageServices interface {
	Save(c Comment) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID CommentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID CommentUUID, vo protocol.VersionOffset) (c Comment, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByType(t Comment_Type, offset, limit uint64) (commentIDs []CommentUUID, nv protocol.NumberOfVersion, err protocol.Error)
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
	Comment_Type_LogActivity
)

/*
	Business Services
*/

type (
	Comment_Service_Register_Request interface {
		GroupID() GroupUUID
		ReplyTo() [16]byte
		UserID() UserUUID
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
