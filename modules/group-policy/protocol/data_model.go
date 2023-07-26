/* For license and copyright information please see the LEGAL file in the code repository */

package gpp

import (
	"memar/protocol"

	gp "org/modules/group/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	GroupID() gp.GroupUUID
	GetPolicy() Policy // Visibility level
	SetPolicy() Policy
	ForwardPolicy() Policy

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
