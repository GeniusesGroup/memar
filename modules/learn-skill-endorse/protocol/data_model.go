/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"

	lsp "org/modules/learn-skill/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID
	SkillID() lsp.SkillUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
