/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type QuestionnaireOrderUUID protocol.UUID

// QuestionnaireOrder indicate the domain record data fields.
type QuestionnaireOrder interface {
	QuestionnaireOrderID() QuestionnaireOrderUUID //
	QuestionnaireID() QuestionnaireUUID           //
	Questions() []QuestionUUID                    //
	Time() protocol.Time                          // Save time
	RequestID() urp.UserRequestUUID               //
}
