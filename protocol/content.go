/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// Content indicate the comment domain record data fields.
type Content interface {
	ContentID() [16]byte        // quiddity domain
	UserID() protocol.UserID    // user domain
	ContentTypeID() [16]byte    // content-type domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type Content_StorageServices interface {
	Save(c Content) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contentID [16]byte, vo protocol.VersionOffset) (c Content, nv protocol.NumberOfVersion, err protocol.Error)

	GetIDs(offset, limit uint64) (contentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	// GetIDsByDateTime(time protocol.Time, offset, limit uint64) (contentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUserID(userID [16]byte, offset, limit uint64) (contentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	FindByType(contentTypeID [16]byte, offset, limit uint64) (contentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
