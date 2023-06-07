/* For license and copyright information please see the LEGAL file in the code repository */

package cp

type GUI_Widget_Conditions interface {
	GroupID() GroupUUID
}

type GUI_Widget_Service interface {
	Pin(cID CommentUUID)
	Unpin(cID CommentUUID)

	// jump to comment location in all comments in the group.
	JumpToCommentPin()
	// render comment-pin page to show all active pinned messages.
	GotoCommentPinPage()
}

type GUI_Page_Conditions interface {
}

type GUI_Page_Service interface {
}
