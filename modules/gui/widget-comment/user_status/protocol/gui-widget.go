/* For license and copyright information please see the LEGAL file in the code repository */

package cus

import (
	"memar/protocol"

	cp "org/modules/comment/protocol"
)

type GUI_Widget_Conditions interface {
	CommentID() cp.CommentUUID
	ViewNumberType() ViewNumberType
	EnableReadBy() bool

	viewNumber()
	time() protocol.Time
}

type GUI_Widget_Service interface {
	// Seen by Whom?
	ReadBy()

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
