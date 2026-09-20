/* For license and copyright information please see the LEGAL file in the code repository */

package qrl_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	label_p "org/modules/knowledge/label/protocol"
	question_p "org/modules/knowledge/question/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	question_p.Field_QuestionID
	Labels() []label_p.UUID

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
