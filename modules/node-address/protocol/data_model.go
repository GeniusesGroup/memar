/* For license and copyright information please see the LEGAL file in the code repository */

package nap

import (
	"memar/protocol"

	np "org/modules/node/protocol"
)

type DataModel interface {
	NodeID() np.UUID
	AddressType() Type
	Address() Address
	AddressBinary() []byte

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// protocol.EventTarget
