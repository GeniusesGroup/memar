/* For license and copyright information please see the LEGAL file in the code repository */

package fap

import (
	"memar/protocol"

	fcp "org/modules/financial-currency/protocol"
	org "org/modules/org/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID FinancialAccountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID FinancialAccountUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_AccountIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (accountIDs []FinancialAccountUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FIND_AccountIDs_BY_SettlementAccountID(settlementAccountID FinancialAccountUUID, offset, limit uint64) (accountIDs []FinancialAccountUUID, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_CurrencyIDs(offset, limit uint64) (currencyIDs []fcp.FinancialCurrencyUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_CurrencyIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (currencyIDs []fcp.FinancialCurrencyUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_SettlementReferences_BY_UserID(userID up.UserUUID, offset, limit uint64) (settlementReferences []org.OrgUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
