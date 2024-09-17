/* For license and copyright information please see the LEGAL file in the code repository */

package trtp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	tp "org/modules/task/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskID() tp.TaskUUID
	OtherID() tp.TaskUUID
	Priority() uint64
	Type() Type

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
