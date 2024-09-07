/* For license and copyright information please see the LEGAL file in the code repository */

// user (delegate usage), ...
package rru_p

import (
	aa_p "org/modules/app-audit/protocol"
	role_p "org/modules/role/protocol"
	storage_p "org/modules/storage/protocol"
	user_p "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	role_p.Field_RoleID
	user_p.Field_UserID
	Type() Type
	Status()

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
