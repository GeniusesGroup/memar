/* For license and copyright information please see the LEGAL file in the code repository */

package cts

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ctp "org/modules/contract-template/protocol"
)

type DataModel interface {
	ContractTemplateID() ctp.ContractTemplateUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
