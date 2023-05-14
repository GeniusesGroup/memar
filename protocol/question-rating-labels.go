/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionRatingLabels indicate the domain record data fields.
type QuestionRatingLabels interface {
	QuestionID() QuestionUUID       //
	Labels() []QuiddityUUID         //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID // user-request domain
}
