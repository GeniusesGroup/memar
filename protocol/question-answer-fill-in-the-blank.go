/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionAnswerFillInTheBlank indicate the domain record data fields.
type QuestionAnswerFillInTheBlank interface {
	AnswerID() AnswerUUID           //
	Answer() []string               //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID // user-request domain
}
