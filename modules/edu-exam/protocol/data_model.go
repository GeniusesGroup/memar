/* For license and copyright information please see the LEGAL file in the code repository */

package exp

import (
	"memar/protocol"

	ekup "org/modules/edu-knowledge_unit/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ExamID() EducationExamUUID
	UserID() up.UserUUID
	KnowledgeUnitID() ekup.EducationKnowledgeUnitUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
