/* For license and copyright information please see the LEGAL file in the code repository */

package crp

import (
	container_p "memar/computer/adt/container/protocol"

	comment_p "org/modules/knowledge/content/edges-loop/comment/protocol"
)

// /discussion?cid=ccccccc&purl=/task?tid=ttttttt
type GUI_Page_Conditions interface {
	comment_p.Field_CommentID
	PageURL() string
	// User

	container_p.Pagination_Offset_Request
}

type GUI_Page_Service interface {
	JumpToRootComment()
	JumpToLastComment()

	// must scroll to group comment in the comment position.
	BackToRootPage()

	LoadMoreUp()
	LoadMoreDown()
}
