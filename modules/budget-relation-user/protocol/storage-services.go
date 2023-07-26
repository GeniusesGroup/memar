/* For license and copyright information please see the LEGAL file in the code repository */

package brup

import (
	"memar/protocol"

	bp "org/modules/budget/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(budgetID bp.BudgetUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(budgetID bp.BudgetUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
