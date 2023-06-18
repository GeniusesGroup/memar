/* For license and copyright information please see the LEGAL file in the code repository */

package fcp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// MoneySettlementReference: https://www.federalreserve.gov/paymentsystems/fedfunds_about.htm
type DataModel interface {
	Currency() FinancialCurrencyUUID // quiddity domain
	// ISO_4217() iso.Currency             //
	MoneySettlementReference() up.UserUUID //can be any org or society user.
	SaveTime() protocol.Time               //
	RequestID() urp.UserRequestUUID        //
}
