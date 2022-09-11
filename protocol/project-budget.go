/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/time/utc"
)

// ProjectBudget indicate the domain record data fields.
type ProjectBudget interface {
	ProjectID() [16]byte           // department domain
	Week() utc.WeekElapsed         //
	Expense() protocol.MoneyAmount //
	Time() protocol.Time           // save time
	RequestID() UserRequestUUID    // user-request domain
}
