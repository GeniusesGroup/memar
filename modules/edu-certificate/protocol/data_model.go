/* For license and copyright information please see the LEGAL file in the code repository */

package ecp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ekup "org/modules/edu-knowledge_unit/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CertificateID() CertificateUUID
	KnowledgeUnitID() ekup.EducationKnowledgeUnitUUID
	IssuedByID() up.UserUUID // organization only??
	IssuedForID() up.UserUUID
	Score() uint64
	IssueTime() protocol.Time

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
