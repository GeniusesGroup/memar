/* For license and copyright information please see the LEGAL file in the code repository */

package fcp

import (
	"libgo/protocol"

	fcp "org/modules/financial-currency/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID                   //
	CurrencyID() fcp.FinancialCurrencyUUID //
	Amount() protocol.MoneyAmount          //
	Balance() protocol.MoneyAmount         //
	SaveTime() protocol.Time               //
	RequestID() urp.UserRequestUUID        //
}
