/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionObject indicate the domain record data fields.
type QuestionObject interface {
	QuestionID() QuestionUUID           //
	MediaTypes() []protocol.MediaTypeID //
	SizeLimit() uint64                  //
	Time() protocol.Time                // Save time
	RequestID() urp.UserRequestUUID     // user-request domain
}
