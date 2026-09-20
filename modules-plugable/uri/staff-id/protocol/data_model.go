/* For license and copyright information please see the LEGAL file in the code repository */

package sip

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	staff_p "org/modules/management/staff/protocol"
)

// TODO::: user-number??
type DataModel interface {
	staff_p.Field_StaffID
	ID() uint32

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
