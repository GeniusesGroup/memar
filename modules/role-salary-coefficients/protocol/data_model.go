/* For license and copyright information please see the LEGAL file in the code repository */

package rscp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	rp "org/modules/role/protocol"
)

type DataModel interface {
	RoleID() rp.RoleUUID //

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

	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
