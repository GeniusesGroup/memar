/* For license and copyright information please see the LEGAL file in the code repository */

package eeqp

import (
	"memar/protocol"

	ekup "org/modules/edu-knowledge_unit/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() EducationQuestionUUID // don't point to quiddity title na don't set title
	UserID() up.UserUUID
	KnowledgeUnitID() ekup.EducationKnowledgeUnitUUID
	Type() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
