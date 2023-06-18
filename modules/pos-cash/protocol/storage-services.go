/* For license and copyright information please see the LEGAL file in the code repository */

package pcp

import (
	"libgo/protocol"

	fap "org/modules/financial-account/protocol"
	pp "org/modules/pos/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(posID pp.PosUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(posID pp.PosUUID, vo protocol.VersionOffset) (dm DataModel, err protocol.Error)

	FIND_PosIDs_BY_AccountID(accountID fap.FinancialAccountUUID, offset, limit uint64) (posIDs []pp.PosUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
