/* For license and copyright information please see the LEGAL file in the code repository */

package label_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	Field_LabelID
	// TODO::: add data fields or delete it

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
