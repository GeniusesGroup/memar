/* For license and copyright information please see the LEGAL file in the code repository */

package lsp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	lp "org/modules/law/protocol"
)

type DataModel interface {
	LawID() lp.LawUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
