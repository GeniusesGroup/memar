/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TaskRepetitive indicate the domain record data fields.
type TaskRepetitive interface {
	TaskID() TaskUUID               //
	Each() uint8                    // Each interval
	Epoch() TaskRepetitive_Epoch    //
	Duration() protocol.Duration    // from Epoch()
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type TaskRepetitive_StorageServices interface {
	Save(dm TaskRepetitive) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(taskID TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(taskID TaskUUID, vo protocol.VersionOffset) (dm TaskRepetitive, nv protocol.NumberOfVersion, err protocol.Error)
}

type TaskRepetitive_Epoch uint8

const (
	TaskRepetitive_Epoch_Unset     TaskRepetitive_Epoch = 0
	TaskRepetitive_Epoch_IssueDate TaskRepetitive_Epoch = (1 << iota)
	TaskRepetitive_Epoch_LastInterval

	TaskRepetitive_Epoch_Continuously
)
