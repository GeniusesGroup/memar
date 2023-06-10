/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type ContentStatus interface {
	ContentID() ContentUUID         //
	Status() Content_Status         //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ContentStatus_StorageServices interface {
	Save(f ContentStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contentID ContentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contentID ContentUUID, vo protocol.VersionOffset) (f ContentStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_ContentIDs_BY_Status(status Content_Status, offset, limit uint64) (contentIDs []ContentUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type Content_Status Quiddity_Status

const (
// Content_Status_ = Content_Status(Quiddity_Status_FreeFlag << iota)
)
