/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	urp "org/modules/user-request/protocol"
)

// BudgetDepartmentRelation indicate the domain record data fields.
type BudgetDepartmentRelation interface {
	BudgetID() BudgetUUID                     //
	DepartmentID() DepartmentUUID             //
	Time() protocol.Time                      // save time
	RequestID() urp.UserRequestUUID           //
}

type BudgetDepartmentRelation_StorageServices interface {
	Save(dm BudgetDepartmentRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID ProjectUUID, accountID FinancialAccountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID ProjectUUID, accountID FinancialAccountUUID, vo protocol.VersionOffset) (dm BudgetDepartmentRelation, nv protocol.NumberOfVersion, err protocol.Error)
}
