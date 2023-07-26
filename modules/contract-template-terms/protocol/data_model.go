/* For license and copyright information please see the LEGAL file in the code repository */

package cttp

import (
	"memar/protocol"

	ctp "org/modules/contract-template/protocol"
)

type DataModel interface {
	ContractTemplateID() ctp.ContractTemplateUUID
	Language() protocol.Language
	Terms() Terms

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
