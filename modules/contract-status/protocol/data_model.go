/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	cp "org/modules/contract/protocol"
)

type DataModel interface {
	ContractID() cp.ContractUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
