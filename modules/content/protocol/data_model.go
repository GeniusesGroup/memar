/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// ContentUUID
// Use in quiddity domain too.
type ContentUUID = protocol.UUID

// Content indicate the domain record data fields.
type Content interface {
	ContentID() ContentUUID         //
	UserID() up.UserUUID            //
	ContentTypeID() ContentTypeUUID // content-type domain
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type Content_StorageServices interface {
	Save(dm Content) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contentID ContentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contentID ContentUUID, vo protocol.VersionOffset) (dm Content, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_ContentIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (contentIDs []ContentUUID, nv protocol.NumberOfVersion, err protocol.Error)
	GetIDs(offset, limit uint64) (contentIDs []ContentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

// FIND_ContentIDs_BY_TypeID(contentTypeID ContentTypeUUID, offset, limit uint64) (contentIDs []ContentUUID, nv protocol.NumberOfVersion, err protocol.Error)
// GetIDsByDateTime(time protocol.Time, offset, limit uint64) (contentIDs []ContentUUID, nv protocol.NumberOfVersion, err protocol.Error)
// FIND_ContentIDs_BY_UserID_AND_TypeID(userID up.UserUUID, contentTypeID ContentTypeUUID, offset, limit uint64) (contentIDs []ContentUUID, nv protocol.NumberOfVersion, err protocol.Error)
