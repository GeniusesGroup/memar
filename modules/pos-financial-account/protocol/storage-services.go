/* For license and copyright information please see the LEGAL file in the code repository */

package pfap

import (
	"memar/protocol"

	fap "org/modules/financial-account/protocol"
	pp "org/modules/pos/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(posID pp.PosUUID, accountID fap.FinancialAccountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(posID pp.PosUUID, accountID fap.FinancialAccountUUID, vo protocol.VersionOffset) (dm DataModel, err protocol.Error)

	LIST_AccountIDs_BY_PosIDs(posID pp.PosUUID, offset, limit uint64) (accountIDs []fap.FinancialAccountUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_PosIDs_BY_AccountID(AccountID fap.FinancialAccountUUID, offset, limit uint64) (posIDs []pp.PosUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
