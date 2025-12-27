/* For license and copyright information please see the LEGAL file in the code repository */

package fcdp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	fcp "org/modules/financial-currency/protocol"
	up "org/modules/user/protocol"
)

// https://en.wikipedia.org/wiki/Credit_card_debt
type DataModel interface {
	UserID() up.UserUUID
	CurrencyID() fcp.FinancialCurrencyUUID
	Amount() protocol.MoneyAmount
	Balance() protocol.MoneyAmount

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// if long overdraft occur, user must pay fee. also can set preference to let system sell its shareholders to overcome of overdraft.
