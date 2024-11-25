/* For license and copyright information please see the LEGAL file in the code repository */

package ptp

import (
	time_p "memar/time/protocol"

	request_p "memar/audit/request/protocol"
	project_p "org/modules/business/project/protocol"

	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	project_p.Field_ProjectID
	ExpectedTime() time_p.Time
	Deadline() time_p.Time

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}
