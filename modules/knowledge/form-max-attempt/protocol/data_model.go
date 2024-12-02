/* For license and copyright information please see the LEGAL file in the code repository */

package fma_p

import (
	request_p "memar/audit/request/protocol"

	form_p "org/modules/knowledge/form/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	form_p.Field_FormID
	MaxAttempt() uint16

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}
