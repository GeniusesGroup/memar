/* For license and copyright information please see the LEGAL file in the code repository */

package trp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	tp "org/modules/task/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskID() tp.TaskUUID
	Each() Each
	Epoch() Epoch
	Duration() protocol.Duration // from Epoch()

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
