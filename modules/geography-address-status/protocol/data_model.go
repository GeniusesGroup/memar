/* For license and copyright information please see the LEGAL file in the code repository */

package uasp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	gap "org/modules/geography-address/protocol"
)

type DataModel interface {
	AddressID() gap.AddressUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
