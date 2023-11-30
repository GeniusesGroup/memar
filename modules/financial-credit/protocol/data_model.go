/* For license and copyright information please see the LEGAL file in the code repository */

package fcp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	fcp "org/modules/financial-currency/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID
	CurrencyID() fcp.FinancialCurrencyUUID
	Amount() protocol.MoneyAmount
	Balance() protocol.MoneyAmount

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
