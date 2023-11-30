/* For license and copyright information please see the LEGAL file in the code repository */

package rrp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
)

type ReactionRate interface {
	ReactionTo() [16]byte // any domain.
	Rate() uint8

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
