/* For license and copyright information please see the LEGAL file in the code repository */

package ttp

import (
	"memar/protocol"

	tp "org/modules/task/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskID() tp.TaskUUID
	ExpectedTime() protocol.Time
	Deadline() protocol.Time

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
