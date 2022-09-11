/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// CommentPin indicate the domain record data fields.
type CommentPin interface {
	CommentID() CommentUUID      // comment domain
	GroupID() [16]byte           // group domain
	CommentPinedID() CommentUUID // comment domain
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

type CommentPin_StorageServices interface {
	Save(cp CommentPin) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(commentID [16]byte) (cp CommentPin, err protocol.Error)

	FindByGroupID(groupID [16]byte, offset, limit uint64) (commentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

// Unpin service : Hidden status to unpin a comment
