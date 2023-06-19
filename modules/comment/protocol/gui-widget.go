/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"libgo/protocol"
)

type GUI_Widget_Conditions interface {
	CommentID() CommentUUID //
	EnablingForwarding() bool

	time() protocol.Time
}

type GUI_Widget_Service interface {
	Save() // TODO::: we need some data model
	Send()
	Reply()
	Forward()
	Edit()
	Delete()
	Pin()
	Report()

	// show a share widget
	Share()
	CopyMessageLink()

	ChangeSenderUser()
}
