/* For license and copyright information please see the LEGAL file in the code repository */

package task_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"
)

// Task indicate the domain record data fields.
type Task interface {
	Field_TaskID
	Field_Type

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
