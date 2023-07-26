/* For license and copyright information please see the LEGAL file in the code repository */

package pap

import (
	"memar/protocol"
	"memar/time/utc"

	pp "org/modules/project/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProjectID() pp.ProjectUUID
	Day() utc.DayElapsed

	TotalTasks() uint64
	CompletedTasks() uint64
	RejectedTasks() uint64
	Progress() uint64
	TaskOverDueTime() uint64 // due time

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
