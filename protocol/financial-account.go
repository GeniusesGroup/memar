/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type FinancialAccountUUID = protocol.UUID

// FinancialAccount indicate the domain record data fields.
type FinancialAccount interface {
	AccountID() FinancialAccountUUID         //
	CurrencyID() FinancialCurrencyUUID       // financial-currency
	UserID() up.UserUUID                     //
	SettlementAccount() FinancialAccountUUID //
	SettlementReference() OrgUUID            // Clearing and Settlement. MoneySettlementReference can be any org or society user.
	SettlementInterval() protocol.Duration   //
	Time() protocol.Time                     // save time
	RequestID() urp.UserRequestUUID          //
}

type FinancialAccount_StorageServices interface {
	Save(fa FinancialAccount) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID [16]byte, vo protocol.VersionOffset) (fa FinancialAccount, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUser(userID up.UserUUID, offset, limit uint64) (accountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	FindBySettlementAccount(SettlementAccount [16]byte, offset, limit uint64) (accountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	ListUserCurrencies(userID up.UserUUID, offset, limit uint64) (currency [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListUserSettlementReferences(userID up.UserUUID, offset, limit uint64) (moneySettlementReferences [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
