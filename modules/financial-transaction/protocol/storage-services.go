/* For license and copyright information please see the LEGAL file in the code repository */

package ftp

import (
	"memar/protocol"

	fap "org/modules/financial-account/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Lock(accountID fap.FinancialAccountUUID) (dm DataModel, err protocol.Error)
	Unlock(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID fap.FinancialAccountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID fap.FinancialAccountUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_AccountSideIDs_BY_AccountID(accountID fap.FinancialAccountUUID, offset, limit uint64) (accountsSideIDs []fap.FinancialAccountUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// TODO::: is it worth to uncomment below service?
	// FindByAccountSideID(accountID, accountSideID [16]byte, offset, limit uint64) (versionOffsets []uint64, nv protocol.NumberOfVersion, err protocol.Error)
}
