/* For license and copyright information please see the LEGAL file in the code repository */

package nrcp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	cp "org/modules/computer/protocol"
	np "org/modules/node/protocol"
)

type DataModel interface {
	NodeID() np.NodeUUID
	ComputerID() cp.ComputerUUID
	RelationType() Type

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
