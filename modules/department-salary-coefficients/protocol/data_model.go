/* For license and copyright information please see the LEGAL file in the code repository */

package dscp

import (
	"memar/math/per"
	"memar/protocol"

	dp "org/modules/department/protocol"
)

// due to organization payment capacity set values to show how many percent add or remove due to organization profit status
type DepartmentSalaryCoefficients interface {
	DepartmentID() dp.DepartmentUUID

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

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
