/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// MoneySettlementReference: https://www.federalreserve.gov/paymentsystems/fedfunds_about.htm
type FinancialCurrency interface {
	Currency() [16]byte // quiddity domain
	// ISO_4217() iso.Currency             //
	MoneySettlementReference() [16]byte // user domain. can be any org or society user.
	Time() protocol.Time                // save time
	RequestID() UserRequestUUID         // user-request domain
}
