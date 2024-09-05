/* For license and copyright information please see the LEGAL file in the code repository */

package dro_p

import (
	aa_p "org/modules/app-audit/protocol"
	department_p "org/modules/org-department/protocol"
	org "org/modules/org/protocol"
	storage_p "org/modules/storage/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	OwnerID() org.OrgUUID
	department_p.Field_DepartmentID

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
