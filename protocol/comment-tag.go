/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// CommentTag indicate the domain record data fields.
// It must just use to index hashtag words from comment-text domain
type CommentTag interface {
	Tag() string            //
	CommentID() CommentUUID // comment domain
	Time() protocol.Time    // save time
}

type CommentTag_StorageServices interface {
	Save(ct CommentTag) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(tag string) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(tag string, vo protocol.VersionOffset) (ct CommentTag, nv protocol.NumberOfVersion, err protocol.Error)

	// TODO:::
}
