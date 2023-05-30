/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// FinancialCredit indicate the domain record data fields.
type FinancialCredit interface {
	UserID() UserUUID               //
	Currency() [16]byte             // financial-currency
	Amount() protocol.MoneyAmount   //
	Balance() protocol.MoneyAmount  //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
