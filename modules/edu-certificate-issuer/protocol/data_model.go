/* For license and copyright information please see the LEGAL file in the code repository */

package ecip

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ekup "org/modules/edu-knowledge_unit/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	IssuerID() up.UserUUID // organization only??
	KnowledgeUnitID() ekup.EducationKnowledgeUnitUUID
	Score() uint64

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
