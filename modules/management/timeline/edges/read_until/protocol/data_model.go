/* For license and copyright information please see the LEGAL file in the code repository */

package cugsp

import (
	cgp "org/modules/knowledge/comment/widgets/group/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ReadUntil() cgp.CommentID
}
