/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type (
	FinancialAccount_StorageService_Save_req interface {
		FinancialAccount
	}
	FinancialAccount_StorageService_Save_res interface {
		NumberOfVersion() protocol.NumberOfVersion
		Error() protocol.Error
	}
)

// type FinancialAccount_StorageServices interface {
// 	Save(fa FinancialAccount) (nv protocol.NumberOfVersion, err protocol.Error)

// 	Count(accountID FinancialAccountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
// 	Get(accountID FinancialAccountUUID, vo protocol.VersionOffset) (fa FinancialAccount, nv protocol.NumberOfVersion, err protocol.Error)

// 	FIND_AccountIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (accountIDs []FinancialAccountUUID, nv protocol.NumberOfVersion, err protocol.Error)
// 	FIND_AccountIDs_BY_SettlementAccountID(settlementAccountID FinancialAccountUUID, offset, limit uint64) (accountIDs []FinancialAccountUUID, nv protocol.NumberOfVersion, err protocol.Error)

// 	LIST_CurrencyIDs(offset, limit uint64) (currencyIDs []FinancialCurrencyUUID, nv protocol.NumberOfVersion, err protocol.Error)
// 	LIST_CurrencyIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (currencyIDs []FinancialCurrencyUUID, nv protocol.NumberOfVersion, err protocol.Error)
// 	LIST_SettlementReferences_BY_UserID(userID up.UserUUID, offset, limit uint64) (settlementReferences []OrgUUID, nv protocol.NumberOfVersion, err protocol.Error)
// }

type FinancialAccount_businessServices interface {
}
