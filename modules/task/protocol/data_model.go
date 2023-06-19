/* For license and copyright information please see the LEGAL file in the code repository */

package tp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// Task indicate the domain record data fields.
type Task interface {
	TaskID() TaskUUID               //
	UserID() up.UserUUID            //
	Type() Type                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_TimeBased
	Type_Repetitive
)
