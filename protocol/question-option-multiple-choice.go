/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionOptionMultipleChoice indicate the domain record data fields.
type QuestionOptionMultipleChoice interface {
	QuestionOptionID() QuestionOptionUUID //
	Min() uint64                          //
	Max() uint64                          //
	Time() protocol.Time                  // Save time
	RequestID() urp.UserRequestUUID       // user-request domain
}
