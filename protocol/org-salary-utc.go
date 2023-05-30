/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// OrgSalaryUTC is fixed salary that use in roles salary rules to calculate each staff salary.
type OrgSalaryUTC interface {
	WeeklySalary() protocol.MoneyAmount // base salary for all staff in organization
	Amount() protocol.MoneyAmount       //
	Time() protocol.Time                // save time
	RequestID() urp.UserRequestUUID     //
}
