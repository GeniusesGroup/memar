/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// CommentUserStatus indicate the domain record data fields.
type CommentUserStatus interface {
	CommentID() CommentUUID         //
	UserID() UserUUID               //
	Status() CommentUser_Status     //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CommentUserStatus_StorageServices interface {
	Save(c CommentUserStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID CommentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID CommentUUID, vo protocol.VersionOffset) (c CommentUserStatus, nv protocol.NumberOfVersion, err protocol.Error)

}

type CommentUser_Status uint8

const (
	CommentUser_Status_Unset CommentUser_Status = iota
	CommentUser_Status_Delivered
	CommentUser_Status_Read
)
