/* For license and copyright information please see the LEGAL file in the code repository */

package bsp

import (
	"libgo/protocol"
	bp "org/modules/budget/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// TODO::: move all budget to the base domain

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID //
	Status() Status
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status
