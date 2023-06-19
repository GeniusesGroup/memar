/* For license and copyright information please see the LEGAL file in the code repository */

package tsp

import (
	"libgo/protocol"

	qsp "org/modules/quiddity-status/protocol"
	tp "org/modules/task/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskID() tp.TaskUUID            //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
	Status_ReadyForDevelopment = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_InProgress
	Status_Close
	Status_Success
)
