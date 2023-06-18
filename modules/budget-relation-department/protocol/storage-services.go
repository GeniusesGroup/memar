/* For license and copyright information please see the LEGAL file in the code repository */

package brdp

import (
	"libgo/protocol"
	bp "org/modules/budget/protocol"
	dp "org/modules/department/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(budgetID bp.BudgetUUID, departmentID dp.DepartmentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(budgetID bp.BudgetUUID, departmentID dp.DepartmentUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
