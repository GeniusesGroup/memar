/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	"libgo/protocol"
	
	cp "org/modules/comment/protocol"
)

// DataModel indicate the domain record data fields.
// It must just use to index hashtag words from comment-text domain
type DataModel interface {
	Tag() string               //
	CommentID() cp.CommentUUID //
	SaveTime() protocol.Time   //
}
