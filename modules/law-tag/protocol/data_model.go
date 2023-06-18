/* For license and copyright information please see the LEGAL file in the code repository */

package ltp

import (
	"libgo/protocol"

	lp "org/modules/law/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel or law hashtag indicate the domain record data fields.
type DataModel interface {
	LawID() lp.LawUUID              //
	Tag() string                    //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
// LawTag_Status_ = Status(Quiddity_Status_FreeFlag << iota)
)
