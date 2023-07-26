/* For license and copyright information please see the LEGAL file in the code repository */

package exap

import (
	"memar/protocol"

	eeqp "org/modules/edu-exam-question/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() eeqp.EducationQuestionUUID
	UserID() up.UserUUID
	Answer() string
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
