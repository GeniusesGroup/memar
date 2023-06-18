/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"libgo/protocol"

	cp "org/modules/comment/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CommentID() cp.CommentUUID      //
	Settings() Settings             //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Settings uint64

const (
	Settings_Unset        Settings = 0
	Settings_PreviewLinks Settings = (1 << iota) // Render web links as small widget or not
	// Authorization
	Settings_Forwardable       // Allow to forward it
	Settings_SilentForwardable // Don't add comment detail like user created
	Settings_NoReply
	Settings_Mute

	Settings_Thread

	Settings_Toxic
	Settings_Spam
	Settings_Sensitivity
	Settings_Confidential // if not set mean normal message
)
