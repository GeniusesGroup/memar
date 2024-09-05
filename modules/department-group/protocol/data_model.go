/* For license and copyright information please see the LEGAL file in the code repository */

package dg_p

import (
	aa_p "org/modules/app-audit/protocol"
	group_p "org/modules/group/protocol"
	department_p "org/modules/org-department/protocol"
	storage_p "org/modules/storage/protocol"
)

type DataModel interface {
	department_p.Field_DepartmentID
	group_p.Field_GroupID
	Status()

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
