/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// PosProvider or pos operator is to supply a particular service.
type PosCash interface {
	PosID() PosUUID                     //
	AccountID() FinancialAccountUUID    //
	MaxCash() protocol.MoneyAmount      //
	MaxCashTransfer() protocol.Duration // from reach the max limit
	Time() protocol.Time                // save time
	RequestID() urp.UserRequestUUID     //
}
