/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// RoleSalary is fixed negotiated salary that don't follow org||department||role salary rules.
type RoleSalary interface {
	RoleID() RoleUUID                   //
	WeeklySalary() protocol.MoneyAmount //
	Time() protocol.Time                // save time
	RequestID() urp.UserRequestUUID     //
}
