/* For license and copyright information please see the LEGAL file in the code repository */

package exqdp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	eeqp "org/modules/edu-exam-question/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() eeqp.EducationQuestionUUID
	Language() protocol.Language
	Question() string      // Content+Presentation(HTML, CSS)
	CorrectAnswer() string // A||B, A&B

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
