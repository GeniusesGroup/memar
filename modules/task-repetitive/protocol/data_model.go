/* For license and copyright information please see the LEGAL file in the code repository */

package trp

import (
	"libgo/protocol"

	tp "org/modules/task/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskID() tp.TaskUUID            //
	Each() uint8                    // Each interval
	Epoch() TaskRepetitive_Epoch    //
	Duration() protocol.Duration    // from Epoch()
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type TaskRepetitive_Epoch uint8

const (
	TaskRepetitive_Epoch_Unset     TaskRepetitive_Epoch = 0
	TaskRepetitive_Epoch_IssueDate TaskRepetitive_Epoch = (1 << iota)
	TaskRepetitive_Epoch_LastInterval

	TaskRepetitive_Epoch_Continuously
)
