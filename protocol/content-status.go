/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type ContentStatus interface {
	ContentID() [16]byte        // content domain
	Status() Content_Status     //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ContentStatus_StorageServices interface {
	Save(cs ContentStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contentID [16]byte, vo protocol.VersionOffset) (cs ContentStatus, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status Content_Status, offset, limit uint64) (contentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type Content_Status Quiddity_Status

const (
// Content_Status_ = Content_Status(Quiddity_Status_FreeFlag << iota)
)
