/* For license and copyright information please see the LEGAL file in the code repository */

package ekup

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	KnowledgeUnitID() EducationKnowledgeUnitUUID
	UserID() up.UserUUID
	Type() Type

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
