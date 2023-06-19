/* For license and copyright information please see the LEGAL file in the code repository */

package crp

import (
	cp "org/modules/comment/protocol"
)

type GUI_Widget_HyperLinks interface {
	// To see all reply to the comment
	NavigateToDiscussionPage()
}

type GUI_Widget_Conditions interface {
	CommentID() cp.CommentUUID //

	replyNumber()
}

type GUI_Widget_Service interface {
}
