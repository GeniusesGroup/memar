/* For license and copyright information please see the LEGAL file in the code repository */

package qrr_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"
	record_p "memar/storage/record/protocol"

	question_p "org/modules/knowledge/question/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	question_p.Field_QuestionID
	RelationIDs() []record_p.UUID // Question, Form
	RelationTypes() []Type

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
