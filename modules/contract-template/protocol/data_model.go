/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
)

type DataModel interface {
	ContractTemplateID() ContractTemplateUUID
	Language() protocol.Language // base language

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
