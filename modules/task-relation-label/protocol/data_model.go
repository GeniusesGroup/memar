/* For license and copyright information please see the LEGAL file in the code repository */

package trlp

import (
	"libgo/protocol"

	lp "org/modules/label/protocol"
	tp "org/modules/task/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskID() tp.TaskUUID            //
	Label() lp.LabelUUID            //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

// default labels:
// 	Type_Compliment
// 	Type_Suggestion
// 	Type_Issue
