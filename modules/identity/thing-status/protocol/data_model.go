/* For license and copyright information please see the LEGAL file in the code repository */

package ts_p

import (
	request_p "memar/audit/request/protocol"

	thing_p "org/modules/identity/thing/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	thing_p.Field_ThingID
	Field_Status

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}
