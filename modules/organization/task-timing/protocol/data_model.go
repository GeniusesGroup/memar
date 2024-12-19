/* For license and copyright information please see the LEGAL file in the code repository */

package ttp

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"
	time_p "memar/time/protocol"

	task_p "org/modules/organization/task/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	task_p.Field_TaskID
	ExpectedTime() time_p.Time
	Deadline() time_p.Time

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
