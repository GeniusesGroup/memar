/* For license and copyright information please see the LEGAL file in the code repository */

package department_p

import (
	aa_p "org/modules/app-audit/protocol"
	storage_p "org/modules/storage/protocol"
)

// DataModel indicate the domain record data fields.
// It can use to show organizational chart. Also staffs can join to the related group.
type DataModel interface {
	Field_DepartmentID
	ParentID() DepartmentUUID // Exist if it isn't top of the organization.

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
