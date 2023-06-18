/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	cp "org/modules/comment/protocol"
	gp "org/modules/group/protocol"
)

type GUI_Widget_Conditions interface {
	GroupID() gp.GroupUUID
}

type GUI_Widget_Service interface {
	Pin(cID cp.CommentUUID)
	Unpin(cID cp.CommentUUID)

	// jump to comment location in all comments in the group.
	JumpToCommentPin()
	// render comment-pin page to show all active pinned messages.
	GotoCommentPinPage()
}

type GUI_Page_Conditions interface {
}

type GUI_Page_Service interface {
}
