/* For license and copyright information please see the LEGAL file in the code repository */

package nsp

import (
	"memar/protocol"

	np "org/modules/node/protocol"
)

type DataModel interface {
	NodeID() np.UUID
	Type() uint8
	ResourceType() []ResourceType
	ResourceAmount() []string

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
