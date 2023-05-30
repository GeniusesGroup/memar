/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type FinancialCurrencyUUID = protocol.UUID

// MoneySettlementReference: https://www.federalreserve.gov/paymentsystems/fedfunds_about.htm
type FinancialCurrency interface {
	Currency() FinancialCurrencyUUID // quiddity domain
	// ISO_4217() iso.Currency             //
	MoneySettlementReference() up.UserUUID //can be any org or society user.
	Time() protocol.Time                   // save time
	RequestID() urp.UserRequestUUID        //
}
