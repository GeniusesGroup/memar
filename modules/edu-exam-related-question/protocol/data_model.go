/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"

	eeqp "org/modules/edu-exam-question/protocol"
	exp "org/modules/edu-exam/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	SuggesterID() up.UserUUID
	ExamID() exp.EducationExamUUID
	Priority() uint64
	QuestionID() eeqp.EducationQuestionUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
