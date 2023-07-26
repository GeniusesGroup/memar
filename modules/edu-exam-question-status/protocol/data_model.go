/* For license and copyright information please see the LEGAL file in the code repository */

package exqsp

import (
	"memar/protocol"

	eeqp "org/modules/edu-exam-question/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() eeqp.EducationQuestionUUID // don't point to quiddity title na don't set title
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
