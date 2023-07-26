/* For license and copyright information please see the LEGAL file in the code repository */

package fasp

import (
	"memar/protocol"

	fap "org/modules/financial-account/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID fap.FinancialAccountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID fap.FinancialAccountUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_AccountIDs_BY_Status(status Status, offset, limit uint64) (accountIDs []fap.FinancialAccountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
