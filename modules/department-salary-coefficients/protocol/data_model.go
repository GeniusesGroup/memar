/* For license and copyright information please see the LEGAL file in the code repository */

package dscp

import (
	"libgo/protocol"

	dp "org/modules/department/protocol"
	urp "org/modules/user-request/protocol"
)

// due to organization payment capacity set values to show how many percent add or remove due to organization profit status
type DepartmentSalaryCoefficients interface {
	DepartmentID() dp.DepartmentUUID //

	Importance() protocol.PerMyriad         // importance coefficient of the department
	Accompanying() protocol.PerMyriad       // Percent for each week
	ExpertiseAllowance() protocol.PerMyriad //
	HardshipAllowance() protocol.PerMyriad  //

	OvertimeWorking() protocol.PerMyriad //
	WorkingHolidays() protocol.PerMyriad //
	RotationShift() protocol.PerMyriad   //
	NightShift() protocol.PerMyriad      //

	Income() protocol.PerMyriad           // whole organization income in each week
	DepartmentIncome() protocol.PerMyriad //

	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
