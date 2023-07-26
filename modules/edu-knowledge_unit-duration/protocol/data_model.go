/* For license and copyright information please see the LEGAL file in the code repository */

package ekudp

import (
	"memar/protocol"

	ekup "org/modules/edu-knowledge_unit/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	KnowledgeUnitID() ekup.EducationKnowledgeUnitUUID
	Minimum() protocol.Duration  // Minimum time duration to learn
	Expected() protocol.Duration // Expected time duration to learn
	Maximum() protocol.Duration  // Maximum time duration to learn

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
