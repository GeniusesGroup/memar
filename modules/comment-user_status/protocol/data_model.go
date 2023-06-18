/* For license and copyright information please see the LEGAL file in the code repository */

package cus

import (
	"libgo/protocol"

	cp "org/modules/comment/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CommentID() cp.CommentUUID      //
	UserID() up.UserUUID            //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status uint8

const (
	Status_Unset Status = iota
	Status_Delivered
	Status_Seen
	Status_Read
)
