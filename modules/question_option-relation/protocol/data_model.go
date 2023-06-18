/* For license and copyright information please see the LEGAL file in the code repository */

package qorp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	qop "org/modules/question_option/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionOptionID() qop.QuestionOptionUUID //
	RelationID() [16]byte                     // Question, Questionnaire
	SaveTime() protocol.Time                  // Save time
	RequestID() urp.UserRequestUUID           //
}
