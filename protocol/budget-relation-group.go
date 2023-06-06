/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	urp "org/modules/user-request/protocol"
)

// BudgetGroupRelation indicate the domain record data fields.
type BudgetGroupRelation interface {
	BudgetID() BudgetUUID //
	GroupID() GroupUUID   //

	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type BudgetGroupRelation_StorageServices interface {
	Save(dm BudgetGroupRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(budgetID BudgetUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(budgetID BudgetUUID, vo protocol.VersionOffset) (dm BudgetGroupRelation, nv protocol.NumberOfVersion, err protocol.Error)
}
