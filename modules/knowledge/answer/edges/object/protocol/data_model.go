/* For license and copyright information please see the LEGAL file in the code repository */

package qaop

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	record_p "memar/storage/record/protocol"
	answer_p "org/modules/knowledge/answer/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	answer_p.Field_AnswerID
	AnswerObject() record_p.UUID

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
