/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type RoleSalaryCoefficients interface {
	RoleID() [16]byte // role domain

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

	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
