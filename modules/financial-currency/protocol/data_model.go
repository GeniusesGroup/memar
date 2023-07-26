/* For license and copyright information please see the LEGAL file in the code repository */

package fcp

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

// MoneySettlementReference: https://www.federalreserve.gov/paymentsystems/fedfunds_about.htm
type DataModel interface {
	Currency() FinancialCurrencyUUID
	// ISO_4217() iso.Currency
	MoneySettlementReference() up.UserUUID //can be any org or society user.

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
