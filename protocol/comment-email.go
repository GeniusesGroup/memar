/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// CommentEmail indicate the domain record data fields.
// TODO::: email subject force to make new comment and save all emails as reply to it in that subject.
type CommentEmail interface {
	CommentID() CommentUUID         //
	From() string                   // name<username@domain>
	To() string                     // name<username@domain>
	CC() string                     // name<username@domain>; name<username@domain>
	BCC() string                    // name<username@domain>
	Subject() string                //
	Senders() []string              // domain
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CommentEmail_StorageServices interface {
	Save(c CommentEmail) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID CommentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID CommentUUID, vo protocol.VersionOffset) (c CommentEmail, nv protocol.NumberOfVersion, err protocol.Error)

	FindByText(text string, offset, limit uint64) (commentIDs []CommentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
