/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CommentID() CommentUUID      //
	UserID() up.UserUUID            //
	Type() Type             //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint32

const (
	Type_Unset Type = 0
	Type_Text  Type = (1 << iota)
	Type_Emoji
	Type_Sticker // gif
	Type_Voice
	Type_File

	Type_MultiParticipant
	Type_Email

	Type_Image
	Type_Video
	Type_Album

	Type_Pin
	Type_Reply
	Type_RelationToComment // Forward, Retweet, Share, ...

	// TODO:::
	Type_LogActivity_PrimaryKey_Single
	Type_LogActivity_PrimaryKey_Double
	Type_LogActivity_PrimaryKey_Triple
	Type_LogActivity_PrimaryKey_String
)
