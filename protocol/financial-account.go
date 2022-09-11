/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type FinancialAccountUUID = protocol.UUID

// FinancialAccount indicate the domain record data fields.
type FinancialAccount interface {
	AccountID() FinancialAccountUUID //
	Currency() [16]byte              // financial-currency
	UserID() protocol.UserID         // user domain
	SettlementAccount() [16]byte     // financial-account domain.
	SettlementReference() [16]byte   // user domain. MoneySettlementReference can be any org or society user.
	Time() protocol.Time             // save time
	RequestID() UserRequestUUID      // user-request domain
}

type FinancialAccount_StorageServices interface {
	Save(fa FinancialAccount) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID [16]byte, vo protocol.VersionOffset) (fa FinancialAccount, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUser(userID [16]byte, offset, limit uint64) (accountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	FindBySettlementAccount(SettlementAccount [16]byte, offset, limit uint64) (accountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	ListUserCurrencies(userID [16]byte, offset, limit uint64) (currency [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListUserSettlementReferences(userID [16]byte, offset, limit uint64) (moneySettlementReferences [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
