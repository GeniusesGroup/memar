/* For license and copyright information please see the LEGAL file in the code repository */

package rscp

import (
	"memar/math/per"
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	rp "org/modules/role/protocol"
)

type DataModel interface {
	RoleID() rp.RoleUUID

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

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
