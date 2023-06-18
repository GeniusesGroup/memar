/* For license and copyright information please see the LEGAL file in the code repository */

package fasp

import (
	"libgo/protocol"

	fap "org/modules/financial-account/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AccountID() fap.FinancialAccountUUID
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
	Status_Closed = Status(qsp.Quiddity_Status_FreeFlag << iota)
)
