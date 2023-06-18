/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	"libgo/protocol"

	cp "org/modules/comment/protocol"
	urp "org/modules/user-request/protocol"
)

// CommentText indicate the domain record data fields.
type DataModel interface {
	CommentID() cp.CommentUUID      //
	Text() string                   // Text With Style. HTML & CSS (No JS) is more expressive than markdown, suggest use them in article text to style text.
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

