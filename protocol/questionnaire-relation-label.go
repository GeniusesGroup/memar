/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionnaireLabel indicate the domain record data fields.
type QuestionnaireLabel interface {
	QuestionnaireID() QuestionnaireUUID //
	Label() LabelUUID                   //
	Time() protocol.Time                // Save time
	RequestID() urp.UserRequestUUID     // user-request domain
}
