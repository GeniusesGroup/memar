/* For license and copyright information please see the LEGAL file in the code repository */

package ta_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"
	"memar/time/utc"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	utc.Field_DayElapsed

	TotalTasks() uint64
	CompletedTasks() uint64
	RejectedTasks() uint64
	Progress() uint64
	TaskOverDueTime() uint64 // due time

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
