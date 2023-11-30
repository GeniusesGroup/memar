/* For license and copyright information please see the LEGAL file in the code repository */

package nap

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	np "org/modules/node/protocol"
)

type DataModel interface {
	NodeID() np.NodeUUID
	AddressType() Type
	Address() Address
	AddressBinary() []byte

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// protocol.EventTarget
