/* For license and copyright information please see the LEGAL file in the code repository */

package ansp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	anp "org/modules/app-node/protocol"
)

type DataModel interface {
	NodeID() anp.NodeUUID
	Status() Status

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
