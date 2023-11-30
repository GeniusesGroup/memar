/* For license and copyright information please see the LEGAL file in the code repository */

package cap

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	cp "org/modules/contract/protocol"
)

type ContractAnalytic interface {
	ContractID() cp.ContractUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
