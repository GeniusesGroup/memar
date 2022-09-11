/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/time/utc"
)

type DepartmentBudgetDetailUTC interface {
	DepartmentID() [16]byte            // department domain
	Week() utc.WeekElapsed             //
	Type() DepartmentBudgetDetail_Type //
	Amount() protocol.MoneyAmount      //
	Time() protocol.Time               // save time
	RequestID() UserRequestUUID        // user-request domain
}
