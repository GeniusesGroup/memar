/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionOptionsOrdering indicate the domain record data fields.
type QuestionOptionsOrdering interface {
	QuestionID() QuestionUUID           //
	CorrectOrder() []QuestionOptionUUID //
	Time() protocol.Time                // Save time
	RequestID() urp.UserRequestUUID     // user-request domain
}
