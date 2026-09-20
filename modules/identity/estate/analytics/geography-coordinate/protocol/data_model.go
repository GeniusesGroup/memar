/* For license and copyright information please see the LEGAL file in the code repository */

package ggcap

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	ggc_p "org/modules/geography/coordinate/protocol"
)

type DataModel interface {
	ggc_p.Field_CoordinateID
	Distance() uint64     // km or ...
	AverageSpeed() uint64 // km/h or ...

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
