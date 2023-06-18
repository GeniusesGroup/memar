/* For license and copyright information please see the LEGAL file in the code repository */

package ttp

import (
	"libgo/protocol"

	tp "org/modules/task/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskID() tp.TaskUUID            // project-task domain
	Type() Type                     //
	SaveTime() protocol.Time        // Save time
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_ManualStart
	Type_ManualTemporaryEnd
	Type_ManualEnd
	Type_Start
	Type_TemporaryEnd
	Type_End
)
