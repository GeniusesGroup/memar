/* For license and copyright information please see the LEGAL file in the code repository */

package pcp

import (
	"libgo/protocol"

	fap "org/modules/financial-account/protocol"
	pp "org/modules/pos/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel or pos operator is to supply a particular service.
type DataModel interface {
	PosID() pp.PosUUID                   //
	AccountID() fap.FinancialAccountUUID //
	MaxCash() protocol.MoneyAmount       //
	MaxCashTransfer() protocol.Duration  // from reach the max limit
	SaveTime() protocol.Time             //
	RequestID() urp.UserRequestUUID      //
}
