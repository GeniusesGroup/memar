/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// CommentUserGroupStatus indicate the domain record data fields.
type CommentUserGroupStatus interface {
	UserID() UserUUID                    //
	GroupID() GroupUUID                  //
	ReadUntil() protocol.NumberOfVersion //
	Time() protocol.Time                 // save time
	RequestID() urp.UserRequestUUID      //
}

type CommentUserGroupStatus_StorageServices interface {
	Save(c CommentUserStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID UserUUID, groupID GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID UserUUID, groupID GroupUUID, vo protocol.VersionOffset) (c CommentUserStatus, nv protocol.NumberOfVersion, err protocol.Error)
}
