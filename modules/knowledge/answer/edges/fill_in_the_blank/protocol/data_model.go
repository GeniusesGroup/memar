/* For license and copyright information please see the LEGAL file in the code repository */

package qafitbp

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	answer_p "org/modules/knowledge/answer/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	answer_p.Field_AnswerID
	Answer() []string

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
