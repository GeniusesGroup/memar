/* For license and copyright information please see the LEGAL file in the code repository */

package facsp

import (
	error_p "memar/process/error/protocol"
	storage_p "memar/storage/protocol"

	account_p "org/modules/economics/account/protocol"
	org_p "org/modules/identity/organization/protocol"
	user_p "org/modules/identity/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err error_p.Error)

	Get(accountID account_p.UUID) (dm DataModel, err error_p.Error)

	FIND_AccountIDs_BY_SettlementAccountID(settlementAccountID account_p.UUID, offset, limit uint64) (accountIDs []account_p.UUID, num storage_p.NumberOfVersion, err error_p.Error)

	LIST_SettlementReferences_BY_UserID(userID user_p.UUID, offset, limit uint64) (settlementReferences []org_p.UUID, num storage_p.NumberOfVersion, err error_p.Error)
}
