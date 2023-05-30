/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type RoleSalaryCoefficients interface {
	RoleID() RoleUUID //

	Importance() protocol.PerMyriad         // importance coefficient of the role
	Accompanying() protocol.PerMyriad       //
	ExpertiseAllowance() protocol.PerMyriad //
	HardshipAllowance() protocol.PerMyriad  //

	OvertimeWorking() protocol.PerMyriad //
	WorkingHolidays() protocol.PerMyriad //
	RotationShift() protocol.PerMyriad   //
	NightShift() protocol.PerMyriad      //

	Income() protocol.PerMyriad          // whole organization income
	DepartmenIncome() protocol.PerMyriad //

	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
