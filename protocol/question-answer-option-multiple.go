/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionAnswerOptionMultiple indicate the domain record data fields.
type QuestionAnswerOptionMultiple interface {
	AnswerID() AnswerUUID           //
	Answer() []uint8                //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID // user-request domain
}
