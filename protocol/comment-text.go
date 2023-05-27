/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// CommentText indicate the domain record data fields.
type CommentText interface {
	CommentID() CommentUUID         //
	Text() string                   // Text With Style. HTML & CSS (No JS) is more expressive than markdown, suggest use them in article text to style text.
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CommentText_StorageServices interface {
	Save(c CommentText) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID [16]byte, vo protocol.VersionOffset) (c CommentText, nv protocol.NumberOfVersion, err protocol.Error)

	FindByText(text string, offset, limit uint64) (commentIDs [16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
