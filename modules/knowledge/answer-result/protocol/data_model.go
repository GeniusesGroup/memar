/* For license and copyright information please see the LEGAL file in the code repository */

package ar_p

import (
	request_p "memar/audit/request/protocol"

	answer_p "org/modules/knowledge/answer/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	answer_p.Field_AnswerID
	Result() Status

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}
