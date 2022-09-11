/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// Comment indicate the comment-settings domain record data fields.
type CommentSettings interface {
	CommentID() CommentUUID     //
	Settings() Comment_Settings //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type CommentSettings_StorageServices interface {
	Save(c CommentSettings) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID [16]byte, vo protocol.VersionOffset) (c CommentSettings, nv protocol.NumberOfVersion, err protocol.Error)
}

type Comment_Settings uint32

const (
	Comment_Settings_Unset        Comment_Settings = 0
	Comment_Settings_PreviewLinks Comment_Settings = (1 << iota) // Render web links as small widget or not
	// Authorization
	Comment_Settings_Forwardable       // Allow to forward it
	Comment_Settings_SilentForwardable // Don't add comment detail like user created
	Comment_Settings_NoReply
)
