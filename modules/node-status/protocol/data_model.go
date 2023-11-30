/* For license and copyright information please see the LEGAL file in the code repository */

package nsp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	np "org/modules/node/protocol"
)

type DataModel interface {
	NodeID() np.NodeUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
