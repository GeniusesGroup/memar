/* For license and copyright information please see the LEGAL file in the code repository */

package cgp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

type GUI_Widget_Conditions interface {
	GroupID() gp.GroupUUID
	UserID() up.UserUUID
	Text() string
	DisableSending() bool
	DisableReply() bool // TODO::: add more type like limit to mentioned users.
	EnablingForwarding() bool

	// Labels() []string
	// DisableReaction() bool
}

type GUI_Widget_Services interface {
	// show object widget
	Attach()

	Send() (err protocol.Error)
	//
	SendSticker()
	AddEmoji()
	Share()

	SortByMostSeen()

	// Select()
	// MarkAsUnRead(cID CommentUUID)
	// SendReaction(cID CommentUUID)
}
