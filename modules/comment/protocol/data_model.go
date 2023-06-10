/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DatModel indicate the domain record data fields.
type DatModel interface {
	CommentID() CommentUUID         //
	UserID() up.UserUUID            //
	Type() Comment_Type             //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Comment_Type uint32

const (
	Comment_Type_Unset Comment_Type = 0
	Comment_Type_Text  Comment_Type = (1 << iota)
	Comment_Type_Emoji
	Comment_Type_Sticker // gif
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
