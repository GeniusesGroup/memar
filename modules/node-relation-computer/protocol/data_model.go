/* For license and copyright information please see the LEGAL file in the code repository */

package nrcp

import (
	"memar/protocol"

	cp "org/modules/computer/protocol"
	np "org/modules/node/protocol"
)

type DataModel interface {
	NodeID() np.UUID
	ComputerID() cp.UUID
	RelationType() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
