/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// CommentUserGroupStatus indicate the domain record data fields.
type CommentUserGroupStatus interface {
	UserID() up.UserUUID                 //
	GroupID() GroupUUID                  //
	ReadUntil() protocol.NumberOfVersion //
	Time() protocol.Time                 // save time
	RequestID() urp.UserRequestUUID      //
}

type CommentUserGroupStatus_StorageServices interface {
	Save(dm CommentUserStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID, groupID GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID, groupID GroupUUID, vo protocol.VersionOffset) (dm CommentUserStatus, nv protocol.NumberOfVersion, err protocol.Error)
}
