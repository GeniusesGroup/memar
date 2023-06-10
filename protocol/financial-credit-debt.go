/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// https://en.wikipedia.org/wiki/Credit_card_debt
type FinancialCreditDebt interface {
	UserID() up.UserUUID            //
	Currency() [16]byte             // financial-currency
	Amount() protocol.MoneyAmount   //
	Balance() protocol.MoneyAmount  //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}


type FinancialCreditDebt_StorageServices interface {
	Save(dm FinancialCreditDebt) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID ) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID , vo protocol.VersionOffset) (dm FinancialCreditDebt, nv protocol.NumberOfVersion, err protocol.Error)
}

// if long overdraft occur, user must pay fee. also can set preference to let system sell its shareholders to overcome of overdraft.
