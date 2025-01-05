/* For license and copyright information please see the LEGAL file in the code repository */

package comment_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_CommentID interface {
	CommentID() UUID
}

type UUID quiddity_p.UUID
