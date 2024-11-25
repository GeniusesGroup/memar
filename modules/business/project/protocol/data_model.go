/* For license and copyright information please see the LEGAL file in the code repository */

package project_p

import (
	request_p "memar/audit/request/protocol"

	user_p "org/modules/identity/user/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	Field_ProjectID
	user_p.Field_UserID

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}
