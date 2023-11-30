/* For license and copyright information please see the LEGAL file in the code repository */

package ekuep

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ekup "org/modules/edu-knowledge_unit/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID
	KnowledgeUnitID() ekup.EducationKnowledgeUnitUUID
	EndorserID() up.UserUUID
	Score() uint64

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
