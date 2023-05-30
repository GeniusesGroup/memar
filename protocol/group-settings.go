/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// GroupCommentDefaults indicate the domain record data fields.
type GroupCommentDefaults interface {
	GroupID() GroupUUID //
	// ArchiveThreadAfter() protocol.Duration //
	BlockedWords() []string            //
	DefaultSettings() Comment_Settings //
	DefaultStatus() Comment_Status     //
	Time() protocol.Time               // save time
	RequestID() urp.UserRequestUUID    //
}

type GroupSettings_StorageServices interface {
	Save(gs GroupCommentDefaults) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID [16]byte, vo protocol.VersionOffset) (gs GroupCommentDefaults, nv protocol.NumberOfVersion, err protocol.Error)
}
