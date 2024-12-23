/* For license and copyright information please see the LEGAL file in the code repository */

package production_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"
)

// DataModel is the structure of production line.
// https://www.zenscale.in/planning
type DataModel interface {
	Field_ProductionID
	Status() Status

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
