/* For license and copyright information please see the LEGAL file in the code repository */

package rrp

import (
	"memar/protocol"
)

type ReactionRate interface {
	ReactionTo() [16]byte // any domain.
	Rate() uint8

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
