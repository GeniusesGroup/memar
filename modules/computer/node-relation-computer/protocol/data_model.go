/* For license and copyright information please see the LEGAL file in the code repository */

package anrcp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	anp "org/modules/app-node/protocol"
	cp "org/modules/computer/protocol"
)

type DataModel interface {
	NodeID() anp.NodeUUID
	ComputerID() cp.ComputerUUID
	RelationType() Type

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
