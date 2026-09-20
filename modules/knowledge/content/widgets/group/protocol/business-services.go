/* For license and copyright information please see the LEGAL file in the code repository */

package cg_p

import (
	comment_p "org/modules/knowledge/content/edges-loop/comment/protocol"
	group_p "org/modules/management/group/protocol"
)

type (
	BS_Register_Request interface {
		group_p.Field_GroupID
		comment_p.Field_CommentID
	}
)
