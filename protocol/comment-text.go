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
	Save(dm CommentText) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID CommentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID CommentUUID, vo protocol.VersionOffset) (dm CommentText, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_CommentIDs_BY_Text(text string, offset, limit uint64) (commentIDs []CommentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
