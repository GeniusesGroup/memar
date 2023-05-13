/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	
	urp "org/modules/user-request/protocol"
)

// QuestionDuration indicate the domain record data fields.
type QuestionDuration interface {
	QuestionID() QuestionUUID       //
	Epoch() QuestionDuration_Epoch  //
	Duration() protocol.Duration    // from Epoch()
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID // user-request domain
}

type QuestionDuration_Epoch uint8

const (
	QuestionDuration_Epoch_Unset QuestionDuration_Epoch = iota
	QuestionDuration_Epoch_IssueDate
	QuestionDuration_Epoch_StartPoint
)
