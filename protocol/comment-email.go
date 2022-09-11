/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// CommentEmail indicate the domain record data fields.
type CommentEmail interface {
	CommentID() CommentUUID     //
	From() string               // name<username@domain>
	To() string                 // name<username@domain>
	CC() string                 // name<username@domain>; name<username@domain>
	BCC() string                // name<username@domain>
	Subject() string            //
	Senders() []string          // domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID //
}

type CommentEmail_StorageServices interface {
	Save(c CommentEmail) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID [16]byte, vo protocol.VersionOffset) (c CommentEmail, nv protocol.NumberOfVersion, err protocol.Error)

	FindByText(text string, offset, limit uint64) (commentIDs [16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
