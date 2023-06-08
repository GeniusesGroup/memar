/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// CommentUserStatus indicate the domain record data fields.
type CommentUserStatus interface {
	CommentID() CommentUUID         //
	UserID() up.UserUUID            //
	Status() CommentUser_Status     //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CommentUserStatus_StorageServices interface {
	Save(dm CommentUserStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID CommentUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID CommentUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm CommentUserStatus, nv protocol.NumberOfVersion, err protocol.Error)

	// TODO::: get view number
}

type CommentUser_Status uint8

const (
	CommentUser_Status_Unset CommentUser_Status = iota
	CommentUser_Status_Delivered
	CommentUser_Status_Read
)
