/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// Comment indicate the domain record data fields.
type CommentSettings interface {
	CommentID() CommentUUID         //
	Settings() Comment_Settings     //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CommentSettings_StorageServices interface {
	Save(dm CommentSettings) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID CommentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID CommentUUID, vo protocol.VersionOffset) (dm CommentSettings, nv protocol.NumberOfVersion, err protocol.Error)
}


type Comment_Settings uint64

const (
	Comment_Settings_Unset        Comment_Settings = 0
	Comment_Settings_PreviewLinks Comment_Settings = (1 << iota) // Render web links as small widget or not
	// Authorization
	Comment_Settings_Forwardable       // Allow to forward it
	Comment_Settings_SilentForwardable // Don't add comment detail like user created
	Comment_Settings_NoReply
	Comment_Settings_Mute

	Comment_Settings_Thread

	Comment_Settings_Toxic
	Comment_Settings_Spam
	Comment_Settings_Sensitivity
	Comment_Settings_Confidential // if not set mean normal message
)
