/* For license and copyright information please see the LEGAL file in the code repository */

package qmp

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	question_p "org/modules/knowledge/question/protocol"
	qop "org/modules/knowledge/question_option/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	question_p.Field_QuestionID
	Matches() []qop.UUID

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
