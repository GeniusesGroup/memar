/* For license and copyright information please see the LEGAL file in the code repository */

package crp

import (
	"memar/protocol"

	cp "org/modules/comment/protocol"
)

type GUI_Page_UsedDomains interface {
	// Comment
	// User
}

// /discussion?cid=ccccccc&purl=/task?tid=ttttttt
type GUI_Page_Conditions interface {
	CommentID() cp.CommentUUID
	PageURL() string

	protocol.Pagination
}

type GUI_Page_Service interface {
	JumpToRootComment()
	JumpToLastComment()

	// must scroll to group comment in the comment position.
	BackToRootPage()

	LoadMoreUp()
	LoadMoreDown()
}
