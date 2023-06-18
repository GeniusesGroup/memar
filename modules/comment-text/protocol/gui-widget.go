/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	cp "org/modules/comment/protocol"
)

type GUI_Widget_Conditions interface {
	CommentID() cp.CommentUUID //

	// It can be same sa overflow in css values
	Overflow()
}

type GUI_Widget_Service interface {
	Save() // TODO::: we need some data model
	Edit()
	CopyText()

	// Open to show all text.
	SeeMore()

	FindMention()

	// TODO::: Text editor widget or inline functionality??
	MakeSensitiveContent()
	HideSensitiveContent()
	ShowSensitiveContent()

	CreateLink()
}
