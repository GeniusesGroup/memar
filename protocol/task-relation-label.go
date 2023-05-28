/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TaskLabel indicate the domain record data fields.
type TaskLabel interface {
	TaskID() TaskUUID               //
	Label() LabelUUID               //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

// default labels:
// 	Task_Type_Compliment
// 	Task_Type_Suggestion
// 	Task_Type_Issue
