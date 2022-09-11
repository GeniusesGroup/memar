/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// FinancialCredit indicate the domain record data fields.
type FinancialCredit interface {
	UserID() protocol.UserID       // user domain
	Currency() [16]byte            // financial-currency
	Amount() protocol.MoneyAmount  //
	Balance() protocol.MoneyAmount //
	Time() protocol.Time           // save time
	RequestID() UserRequestUUID    // user-request domain
}
