/* For license and copyright information please see the LEGAL file in the code repository */

package cap

import (
	"memar/protocol"

	cp "org/modules/contract/protocol"
)

type ContractAnalytic interface {
	ContractID() cp.ContractUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
