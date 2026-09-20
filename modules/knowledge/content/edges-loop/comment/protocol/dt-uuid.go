/* For license and copyright information please see the LEGAL file in the code repository */

package comment_p

import (
	content_p "org/modules/knowledge/content/protocol"
)

type Field_CommentID interface {
	CommentID() UUID
}

type UUID content_p.UUID
