/* For license and copyright information please see the LEGAL file in the code repository */

package membership_term_member_limit_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	group_p "org/modules/management/group/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	group_p.Field_GroupID

	Minimum() int32  // Minimum number of employees for this job position
	Expected() int32 // Expected number of employees for this job position
	Maximum() int32  // Maximum number of employees for this job position

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
