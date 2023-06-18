/* For license and copyright information please see the LEGAL file in the code repository */

package psp

import (
	"libgo/protocol"

	pp "org/modules/pos/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	PosID() pp.PosUUID              //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
	Pos_Status_CashLimitInactivated = Status(qsp.Quiddity_Status_FreeFlag << iota)
)
