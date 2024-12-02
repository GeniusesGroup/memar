/* For license and copyright information please see the LEGAL file in the code repository */

package fr_p

import (
	request_p "memar/audit/request/protocol"

	user_p "org/modules/identity/user/protocol"
	form_p "org/modules/knowledge/form/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	Field_FormRespondentID
	form_p.Field_FormID
	AnswerBy() user_p.UUID
	FillBy() user_p.UUID

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}
