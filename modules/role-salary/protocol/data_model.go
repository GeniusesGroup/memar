/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// RoleSalary is fixed negotiated salary that don't follow org||department||role salary rules.
type RoleSalary interface {
	RoleID() RoleUUID //
	CurrencyID() FinancialCurrencyUUID
	WeeklySalary() protocol.MoneyAmount //
	Time() protocol.Time                // save time
	RequestID() urp.UserRequestUUID     //
}

type RoleSalary_StorageServices interface {
	Save(dm RoleSalary) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID RoleUUID, vo protocol.VersionOffset) (dm RoleSalary, nv protocol.NumberOfVersion, err protocol.Error)
}
