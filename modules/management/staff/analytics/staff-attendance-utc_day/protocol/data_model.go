/* For license and copyright information please see the LEGAL file in the code repository */

package saa_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"
	"memar/time/earth"
	"memar/time/utc"

	staff_p "org/modules/management/staff/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	staff_p.Field_StaffID
	utc.Field_DayElapsed
	earth.Field_Hour

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
