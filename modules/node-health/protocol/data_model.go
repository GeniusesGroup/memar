/* For license and copyright information please see the LEGAL file in the code repository */

package oip

import (
	"memar/protocol"

	np "org/modules/node/protocol"
)

type DataModel interface {
	NodeID() np.UUID
	SideNodeID() np.UUID
	PingTime() protocol.Duration
	JitterTime() protocol.Duration

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
