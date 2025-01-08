/* For license and copyright information please see the LEGAL file in the code repository */

package dsc_p

import (
	"memar/math/per"

	aa_p "org/modules/app-audit/protocol"
	department_p "org/modules/org-department/protocol"
	storage_p "org/modules/storage/protocol"
)

// due to organization payment capacity set values to show how many percent add or remove due to organization profit status
type DepartmentSalaryCoefficients interface {
	department_p.Field_DepartmentID

	Importance() per.Myriad         // importance coefficient of the department
	Accompanying() per.Myriad       // Percent for each week
	ExpertiseAllowance() per.Myriad //
	HardshipAllowance() per.Myriad  //

	OvertimeWorking() per.Myriad //
	WorkingHolidays() per.Myriad //
	RotationShift() per.Myriad   //
	NightShift() per.Myriad      //

	Income() per.Myriad           // whole organization income in each week
	DepartmentIncome() per.Myriad //

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
