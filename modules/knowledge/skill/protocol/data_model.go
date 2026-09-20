/* For license and copyright information please see the LEGAL file in the code repository */

package skill_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	Field_SkillID
	// TODO::: ??

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
