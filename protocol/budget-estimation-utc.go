/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"
	urp "org/modules/user-request/protocol"
)

// OrgBudgetEstimationUTC is weekly budget domain
// It is potential income that org can produce if anything goes correctly.
type OrgBudgetEstimationUTC interface {
	Week() utc.WeekElapsed          //
	Income() protocol.MoneyAmount   //
	Outcome() protocol.MoneyAmount  //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
