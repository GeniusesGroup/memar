/* For license and copyright information please see the LEGAL file in the code repository */

package fd_p

import (
	request_p "memar/audit/request/protocol"
	"memar/time/duration"
	"memar/time/epoch"

	form_p "org/modules/knowledge/form/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	form_p.Field_FormID
	epoch.Field_DynamicEpoch
	Duration() duration.Second // from Epoch()

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}
