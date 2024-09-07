/* For license and copyright information please see the LEGAL file in the code repository */

package rscp

import (
	"memar/math/per"

	aa_p "org/modules/app-audit/protocol"
	role_p "org/modules/role/protocol"
	storage_p "org/modules/storage/protocol"
)

type DataModel interface {
	role_p.Field_RoleID

	Importance() per.Myriad         // importance coefficient of the role
	Accompanying() per.Myriad       //
	ExpertiseAllowance() per.Myriad //
	HardshipAllowance() per.Myriad  //

	OvertimeWorking() per.Myriad //
	WorkingHolidays() per.Myriad //
	RotationShift() per.Myriad   //
	NightShift() per.Myriad      //

	Income() per.Myriad           // whole organization income
	DepartmentIncome() per.Myriad //

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
