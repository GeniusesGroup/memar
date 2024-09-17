/* For license and copyright information please see the LEGAL file in the code repository */

package ekurp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ekup "org/modules/edu-knowledge_unit/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	SuggesterID() up.UserUUID
	Side1() ekup.EducationKnowledgeUnitUUID
	Priority() uint64
	Level() uint64
	Side2() ekup.EducationKnowledgeUnitUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
