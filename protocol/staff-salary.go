/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// StaffSalary is fixed negotiated salary that don't follow org||department||role salary rules.
type StaffSalary interface {
	StaffID() StaffUUID                 //
	WeeklySalary() protocol.MoneyAmount //
	Time() protocol.Time                // save time
	RequestID() urp.UserRequestUUID     //
}
