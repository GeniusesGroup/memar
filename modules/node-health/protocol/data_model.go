/* For license and copyright information please see the LEGAL file in the code repository */

package oip

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	np "org/modules/node/protocol"
)

type DataModel interface {
	NodeID() np.NodeUUID
	SideNodeID() np.NodeUUID
	PingTime() protocol.Duration
	JitterTime() protocol.Duration

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
