/* For license and copyright information please see the LEGAL file in the code repository */

package vacuh

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"
	"memar/time/utc"

	fmp "org/modules/economics/money/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	utc.Field_HourElapsed
	TotalIssued() uint64
	TotalIssuedAmount() fmp.Amount

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
