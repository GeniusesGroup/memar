/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"
	urp "org/modules/user-request/protocol"
)

// TODO::: move all budget to the base domain

// ProjectBudget indicate the domain record data fields.
type ProjectBudget interface {
	ProjectID() ProjectUUID         //
	Week() utc.WeekElapsed          //
	Income() protocol.MoneyAmount   //
	Outcome() protocol.MoneyAmount  // Expense
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
