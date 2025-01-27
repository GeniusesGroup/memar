/* For license and copyright information please see the LEGAL file in the code repository */

package cugsp

import (
	cgp "org/modules/gui/widget-comment/group/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ReadUntil() cgp.CommentID
}
