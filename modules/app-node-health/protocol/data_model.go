/* For license and copyright information please see the LEGAL file in the code repository */

package anhp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	anp "org/modules/app-node/protocol"
)

type DataModel interface {
	NodeID() anp.NodeUUID
	SideNodeID() anp.NodeUUID
	PingTime() protocol.Duration
	JitterTime() protocol.Duration

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
