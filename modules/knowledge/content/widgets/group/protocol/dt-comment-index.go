/* For license and copyright information please see the LEGAL file in the code repository */

package cg_p

import (
	container_p "memar/computer/adt/container/protocol"
)

type Field_CommentIndex interface {
	CommentIndex() CommentID
}

type CommentID container_p.ElementIndex
