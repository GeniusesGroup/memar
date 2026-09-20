/* For license and copyright information please see the LEGAL file in the code repository */

package transaction_p

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	fa_p "org/modules/economics/account/protocol"
)

type StorageServices interface {
	// Save(dm DataModel) (err error_p.Error)

	// Get_BY_StepNumber(accountID fa_p.UUID, ts StepNumber) (dm DataModel, err error_p.Error)
	// Get_BY_TransactionID(accountID fa_p.UUID, tID UUID) (dm DataModel, err error_p.Error)

	LIST_AccountSideIDs_BY_AccountID(accountID fa_p.UUID, offset, limit uint64) (accountsSideIDs []fa_p.UUID, num storage_p.NumberOfVersion, err error_p.Error)

	// TODO::: is it worth to uncomment below service?
	// Find_TransactionID_BY_AccountIDs(accountID, accountSideID account_p.UUID, offset, limit uint64) (tID []TransactionID, nv storage_p.NumberOfVersion, err error_p.Error)
}
