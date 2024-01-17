/* For license and copyright information please see the LEGAL file in the code repository */

package anap

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	anp "org/modules/app-node/protocol"
)

type DataModel interface {
	NodeID() anp.NodeUUID
	AddressType() Type
	Address() Address
	AddressBinary() []byte

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// protocol.EventTarget
