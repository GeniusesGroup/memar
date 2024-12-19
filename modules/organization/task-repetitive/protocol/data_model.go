/* For license and copyright information please see the LEGAL file in the code repository */

package tr_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"
	"memar/time/duration"
	"memar/time/epoch"

	task_p "org/modules/organization/task/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	task_p.Field_TaskID
	Field_Each
	epoch.Field_DynamicEpoch
	Duration() duration.Second // from Epoch()

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
