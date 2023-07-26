/* For license and copyright information please see the LEGAL file in the code repository */

package qaomp

import (
	"memar/protocol"

	qap "org/modules/question_answer/protocol"
	qop "org/modules/question_option/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AnswerID() qap.AnswerUUID
	Answer() []qop.QuestionOptionUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
