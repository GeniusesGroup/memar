/* For license and copyright information please see the LEGAL file in the code repository */

package qmap

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	question_p "org/modules/knowledge/question/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	question_p.Field_QuestionID
	MaxAttempt() uint16

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
