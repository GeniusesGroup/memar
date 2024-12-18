/* For license and copyright information please see the LEGAL file in the code repository */

package ls_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"

	label_p "org/modules/knowledge/label/protocol"
)

type DataModel interface {
	label_p.Field_LabelID
	Field_Status

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
