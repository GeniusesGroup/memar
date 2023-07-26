/* For license and copyright information please see the LEGAL file in the code repository */

package udp

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

// DataModel is unique name in the computer world. Country e.g. Iran, ... || Digital platforms e.g. Instagram, Facebook, Google, Github, Yahoo, ...
type DataModel interface {
	Domain() string // unique name in the computer world
	UserID() up.UserUUID
	AcceptedProtocols() UserDomain_AP
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
