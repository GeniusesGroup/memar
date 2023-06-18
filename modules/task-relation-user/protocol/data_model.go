/* For license and copyright information please see the LEGAL file in the code repository */

package trup

import (
	"libgo/protocol"

	tp "org/modules/task/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskID() tp.TaskUUID            //
	UserID() up.UserUUID            //
	RelationType() Type             //
	SaveTime() protocol.Time        // Save time
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_Participant
	Type_Assigner
	Type_Assigned
	Type_Reviewer
	Type_Approver
)
