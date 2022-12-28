/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"
)

// OrgBudgetEstimationUTC is weekly budget domain
type DepartmentBudgetEstimationUTC interface {
	DepartmentID() [16]byte        // department domain
	Week() utc.WeekElapsed         //
	Income() protocol.MoneyAmount  //
	Outcome() protocol.MoneyAmount //
	Time() protocol.Time           // save time
	RequestID() UserRequestUUID    // user-request domain
}
