/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"libgo/protocol"
)

type GUI_Widget_Conditions interface {
	CommentID() CommentUUID //
	ViewNumberType() ViewNumberType
	EnableReadBy() bool
	EnablingForwarding() bool

	viewNumber()
	replyNumber()
	time() protocol.Time
}

type GUI_Widget_Service interface {
	Save() // TODO::: we need some data model
	Reply()
	Forward()
	Edit()
	Delete()
	Pin()
	Report()

	// show a share widget
	Share()
	CopyMessageLink()

	// Seen by Whom?
	ReadBy()

	ChangeSenderUser()

	// set to see by the user.
	Seen()

	getViewNumber()
}

type ViewNumberType uint8

const (
	ViewNumberType_Unset ViewNumberType = iota
	ViewNumberType_ShowNumber
	// Just show ticket that first use read the comment.
	ViewNumberType_ShowTick
)
