/* For license and copyright information please see the LEGAL file in the code repository */

package lsp

import (
	"libgo/protocol"

	lp "org/modules/law/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	LawID() lp.LawUUID              //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
	Status_Suggestion = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_Closed
	Status_Approved
	Status_Denied
)
