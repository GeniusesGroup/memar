/* For license and copyright information please see the LEGAL file in the code repository */

package lsp

import (
	"memar/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	SkillID() SkillUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
