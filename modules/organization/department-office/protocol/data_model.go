/* For license and copyright information please see the LEGAL file in the code repository */

package do_p

import (
	aa_p "org/modules/app-audit/protocol"
	blp "org/modules/estate-building-location/protocol"
	department_p "org/modules/org-department/protocol"
	storage_p "org/modules/storage/protocol"
)

type DataModel interface {
	department_p.Field_DepartmentID
	BuildingLocationID() blp.BuildingLocationUUID
	// TODO::: Label or type: IT-Office, ...

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
