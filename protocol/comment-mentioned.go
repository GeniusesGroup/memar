/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// CommentMentioned indicate the domain record data fields.
type CommentMentioned interface {
	UserID() protocol.UserID // user domain
	CommentID() CommentUUID  // comment domain
	Time() protocol.Time     // save time
}

type CommentMentioned_StorageServices interface {
	Save(cm CommentMentioned) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID [16]byte, vo protocol.VersionOffset) (cm CommentMentioned, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}
