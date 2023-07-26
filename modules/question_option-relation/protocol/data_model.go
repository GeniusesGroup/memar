/* For license and copyright information please see the LEGAL file in the code repository */

package qorp

import (
	"memar/protocol"

	qop "org/modules/question_option/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionOptionID() qop.QuestionOptionUUID
	RelationID() [16]byte // Question, Questionnaire

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
