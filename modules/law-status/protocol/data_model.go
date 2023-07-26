/* For license and copyright information please see the LEGAL file in the code repository */

package lsp

import (
	"memar/protocol"

	lp "org/modules/law/protocol"
)

type DataModel interface {
	LawID() lp.LawUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
