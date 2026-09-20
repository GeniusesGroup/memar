/* For license and copyright information please see the LEGAL file in the code repository */

package cp_p

import (
	comment_p "org/modules/knowledge/content/edges-loop/comment/protocol"
	group_p "org/modules/management/group/protocol"
)

type GUI_Widget_Conditions interface {
	group_p.Field_GroupID
}

type GUI_Widget_Service interface {
	Pin(cID comment_p.UUID)
	Unpin(cID comment_p.UUID)

	// jump to comment location in all comments in the group.
	JumpToCommentPin()
	// render comment-pin page to show all active pinned messages.
	GotoCommentPinPage()
}

type GUI_Page_Conditions interface {
}

type GUI_Page_Service interface {
}
