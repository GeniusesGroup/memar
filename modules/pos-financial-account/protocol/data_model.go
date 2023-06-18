/* For license and copyright information please see the LEGAL file in the code repository */

package pfap

import (
	"libgo/protocol"

	fap "org/modules/financial-account/protocol"
	pp "org/modules/pos/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel or pos operator is to supply a particular service.
type DataModel interface {
	PosID() pp.PosUUID                   //
	AccountID() fap.FinancialAccountUUID //
	Status() Status
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status
