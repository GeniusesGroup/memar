/* For license and copyright information please see the LEGAL file in the code repository */

package fai

import (
	"libgo/protocol"

	fap "org/modules/financial-account/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID fap.FinancialAccountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID fap.FinancialAccountUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_AccountIDs_BY_ID(id string) (accountIDs []fap.FinancialAccountUUID, err protocol.Error)
}
