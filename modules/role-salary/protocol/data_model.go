/* For license and copyright information please see the LEGAL file in the code repository */

package rsp

import (
	"libgo/protocol"

	fcp "org/modules/financial-currency/protocol"
	rp "org/modules/role/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel is fixed negotiated salary that don't follow org||department||role salary rules.
type DataModel interface {
	RoleID() rp.RoleUUID                   //
	CurrencyID() fcp.FinancialCurrencyUUID //
	WeeklySalary() protocol.MoneyAmount    //
	SaveTime() protocol.Time               //
	RequestID() urp.UserRequestUUID        //
}
