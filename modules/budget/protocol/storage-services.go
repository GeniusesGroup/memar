/* For license and copyright information please see the LEGAL file in the code repository */

package bp

import (
	"memar/protocol"

	org "org/modules/org/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(budgetID BudgetUUID, orgID org.OrgUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(budgetID BudgetUUID, orgID org.OrgUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
