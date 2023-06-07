/* For license and copyright information please see the LEGAL file in the code repository */

package cgp

import (
	"libgo/protocol"
	up "org/modules/user/protocol"
)

type GUI_Widget_Conditions interface {
	GroupID() GroupUUID
	UserID() up.UserUUID
	Text() string
	DisableSending() bool
}

type GUI_Widget_Services interface {
	// Open a dialog to choose attach files
	Attach()
	Send() (err protocol.Error)
	//
	SendSticker()
	AddEmoji()
	Share()
}

type GUI_Widget_Conditions interface {
	Labels() []string
	DisableReaction() bool
}

type GUI_Widget_Service interface {
	Select()
	MarkAsUnRead(cID CommentUUID)
	SendReaction(cID CommentUUID)
}
