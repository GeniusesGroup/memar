/* For license and copyright information please see the LEGAL file in the code repository */

package ekusp

import (
	"memar/protocol"

	ekup "org/modules/edu-knowledge_unit/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID
	KnowledgeUnitID() ekup.EducationKnowledgeUnitUUID
	GivenScoreID() up.UserUUID
	LearnDuration() protocol.Duration
	Score() uint64

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
