/* For license and copyright information please see the LEGAL file in the code repository */

package tcp

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"

	task_p "org/modules/organization/task/protocol"
)

// DataModel indicate the domain record data fields.
// a basis for comparison; a reference point against which other things can be evaluated
// the ideal in terms of which something can be judged
type DataModel interface {
	task_p.Field_TaskID
	Field_Type
	Field_Point

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
