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
	Save(dm GroupCommentDefaults) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID GroupUUID, vo protocol.VersionOffset) (dm GroupCommentDefaults, nv protocol.NumberOfVersion, err protocol.Error)
    
	
}
