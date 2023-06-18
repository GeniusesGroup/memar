/* For license and copyright information please see the LEGAL file in the code repository */

package famp

import (
	"libgo/protocol"

	fap "org/modules/financial-account/protocol"
	fcp "org/modules/financial-currency/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID //
	Currency() fcp.FinancialCurrencyUUID
	AccountID() fap.FinancialAccountUUID
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
