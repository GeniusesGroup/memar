/* For license and copyright information please see the LEGAL file in the code repository */

package brep

import (
	bp "org/modules/budget/protocol"
	"libgo/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(budgetID bp.BudgetUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(budgetID bp.BudgetUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
