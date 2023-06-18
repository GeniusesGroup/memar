/* For license and copyright information please see the LEGAL file in the code repository */

package osup

import (
	"libgo/protocol"

	fcp "org/modules/financial-currency/protocol"
	org "org/modules/org/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel is fixed salary that use in roles salary rules to calculate each staff salary.
type DataModel interface {
	OrgID() org.OrgUUID
	CurrencyID() fcp.FinancialCurrencyUUID //
	Amount() protocol.MoneyAmount          //
	SaveTime() protocol.Time               //
	RequestID() urp.UserRequestUUID        //
}

