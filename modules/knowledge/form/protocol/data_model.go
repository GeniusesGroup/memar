/* For license and copyright information please see the LEGAL file in the code repository */

package form_p

import (
	request_p "memar/audit/request/protocol"

	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	Field_FormID
	Field_Type

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}
