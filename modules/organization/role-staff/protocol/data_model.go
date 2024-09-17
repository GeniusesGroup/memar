/* For license and copyright information please see the LEGAL file in the code repository */

package rsp

import (
	aa_p "org/modules/app-audit/protocol"
	role_p "org/modules/role/protocol"
	storage_p "org/modules/storage/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	role_p.Field_RoleID
	Minimum() int32  // Minimum number of employees for this job position
	Expected() int32 // Expected number of employees for this job position
	Maximum() int32  // Maximum number of employees for this job position

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
