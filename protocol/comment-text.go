/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// CommentText indicate the domain record data fields.
type CommentText interface {
	CommentID() CommentUUID     // comment domain
	Text() string               // Text With Style. HTML & CSS (No JS) is more expressive than markdown, suggest use them in article text to style text.
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type CommentText_StorageServices interface {
	Save(c CommentText) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID [16]byte, vo protocol.VersionOffset) (c CommentText, nv protocol.NumberOfVersion, err protocol.Error)

	FindByText(text string, offset, limit uint64) (commentIDs [16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
