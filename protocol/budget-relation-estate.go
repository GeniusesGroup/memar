/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	urp "org/modules/user-request/protocol"
)

// BudgetEstateRelation indicate the domain record data fields.
type BudgetEstateRelation interface {
	BudgetID() BudgetUUID                     //
	EstateID() EstateUUID                     //
	BuildingLocationID() BuildingLocationUUID //
	Time() protocol.Time                      // save time
	RequestID() urp.UserRequestUUID           //
}

type BudgetDepartment_StorageServices interface {
	Save(dm BudgetEstateRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID ProjectUUID, accountID FinancialAccountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID ProjectUUID, accountID FinancialAccountUUID, vo protocol.VersionOffset) (dm BudgetEstateRelation, nv protocol.NumberOfVersion, err protocol.Error)
}
