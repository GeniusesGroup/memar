/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// RoleSalary is fixed negotiated salary that don't follow org||department||role salary rules.
type RoleSalary interface {
	RoleID() [16]byte                   // role domain
	WeeklySalary() protocol.MoneyAmount //
	Time() protocol.Time                // save time
	RequestID() UserRequestUUID         // user-request domain
}
