/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ContentDuration indicate the domain record data fields.
type ContentDuration interface {
	ContentID() ContentUUID
	Duration() protocol.Duration    // AI suggested duration
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ContentDuration_StorageServices interface {
	Save(dm ContentDuration) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contentID ContentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contentID ContentUUID, vo protocol.VersionOffset) (dm ContentDuration, nv protocol.NumberOfVersion, err protocol.Error)
}
