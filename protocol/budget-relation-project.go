/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	urp "org/modules/user-request/protocol"
)

// BudgetProject indicate the domain record data fields.
type BudgetProject interface {
	BudgetID() BudgetUUID           //
	ProjectID() ProjectUUID         //
	TaskID() TaskUUID               //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type BudgetProject_StorageServices interface {
	Save(dm BudgetProject) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(budgetID BudgetUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(budgetID BudgetUUID, vo protocol.VersionOffset) (dm BudgetProject, nv protocol.NumberOfVersion, err protocol.Error)
}
