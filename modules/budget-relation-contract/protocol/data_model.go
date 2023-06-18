/* For license and copyright information please see the LEGAL file in the code repository */

package brcp

import (
	"libgo/protocol"
	bp "org/modules/budget/protocol"
	cp "org/modules/contract/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID        //
	ContractID() cp.ContractUUID    //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status
