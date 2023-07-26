/* For license and copyright information please see the LEGAL file in the code repository */

package ip

import (
	"memar/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InviteID() InviteUUID
	Type() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// TODO::: user send last time of active state record plus its ID and optional invited user id as invite code.
