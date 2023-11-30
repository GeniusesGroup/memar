/* For license and copyright information please see the LEGAL file in the code repository */

package qapsp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	qap "org/modules/question_answer/protocol"
	qop "org/modules/question_option/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AnswerID() qap.AnswerUUID
	Answer() qop.QuestionOptionUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
