/* For license and copyright information please see the LEGAL file in the code repository */

package trtp

import (
	"libgo/protocol"

	tp "org/modules/task/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskID() tp.TaskUUID            //
	OtherID() tp.TaskUUID           //
	Priority() uint64               //
	Type() Type                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset      Type = 0
	Type_Complement Type = (1 << iota)
	Type_Blocking
)
