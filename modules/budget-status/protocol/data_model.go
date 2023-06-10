/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	urp "org/modules/user-request/protocol"
)

// TODO::: move all budget to the base domain

// BudgetStatus indicate the domain record data fields.
type BudgetStatus interface {
	BudgetID() BudgetUUID //
	Status() Budget_Status
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type BudgetStatus_StorageServices interface {
	Save(dm Budget) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(budgetID BudgetUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(budgetID BudgetUUID, vo protocol.VersionOffset) (dm Budget, nv protocol.NumberOfVersion, err protocol.Error)
}

type Budget_Status Quiddity_Status
