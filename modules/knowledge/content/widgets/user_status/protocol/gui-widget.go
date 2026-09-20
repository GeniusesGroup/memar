/* For license and copyright information please see the LEGAL file in the code repository */

package cus_p

import (
	time_p "memar/time/protocol"
	comment_p "org/modules/knowledge/content/edges-loop/comment/protocol"
)

type GUI_Widget_Conditions interface {
	comment_p.Field_CommentID
	ViewNumberType() ViewNumberType
	EnableReadBy() bool

	viewNumber()
	time() time_p.Time
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
