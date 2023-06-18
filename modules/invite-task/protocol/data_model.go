/* For license and copyright information please see the LEGAL file in the code repository */

package itp

import (
	"libgo/protocol"

	ip "org/modules/invite/protocol"
	tp "org/modules/task/protocol"
	urp "org/modules/user-request/protocol"
)

// TODO::: Optional module

// DataModel indicate the domain record data fields.
type DataModel interface {
	InviteID() ip.InviteUUID        //
	TaskID() tp.TaskUUID            //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
