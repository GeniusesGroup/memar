/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	"memar/protocol"
)

type DataModel interface {
	ContractTemplateID() ContractTemplateUUID
	Language() protocol.Language // base language

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
