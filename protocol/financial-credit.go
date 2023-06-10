/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// FinancialCredit indicate the domain record data fields.
type FinancialCredit interface {
	UserID() up.UserUUID            //
	Currency() [16]byte             // financial-currency
	Amount() protocol.MoneyAmount   //
	Balance() protocol.MoneyAmount  //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type FinancialCredit_StorageServices interface {
	Save(dm FinancialCredit) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID ) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID , vo protocol.VersionOffset) (dm FinancialCredit, nv protocol.NumberOfVersion, err protocol.Error)
}