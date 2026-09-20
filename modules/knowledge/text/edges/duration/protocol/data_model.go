/* For license and copyright information please see the LEGAL file in the code repository */

package cdp

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"
	"memar/time/duration"

	text_p "org/modules/knowledge/text/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	text_p.Field_TextUUID
	duration.Field_Second // AI suggested duration

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
