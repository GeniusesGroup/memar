/* For license and copyright information please see the LEGAL file in the code repository */

package ttp

import (
	"libgo/protocol"

	tp "org/modules/task/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskID() tp.TaskUUID            //
	ExpectedTime() protocol.Time    //
	Deadline() protocol.Time        //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
