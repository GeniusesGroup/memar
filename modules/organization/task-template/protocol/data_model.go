/* For license and copyright information please see the LEGAL file in the code repository */

package ttp

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"

	user_p "org/modules/identity/user/protocol"
)

// TODO::: task can be use as template, Need this module?

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskTemplateID() TaskTemplateUUID
	user_p.Field_UserID
	// TODO::: group of comment?? business form??

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
