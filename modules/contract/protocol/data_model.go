/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"memar/protocol"

	ctp "org/modules/contract-template/protocol"
)

type DataModel interface {
	ContractID() ContractUUID
	ContractTemplateID() ctp.ContractTemplateUUID
	ContractTemplateVersion() protocol.VersionOffset
	Data() map[Type]string

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// Service: fulfill the obligation
