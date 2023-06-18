/* For license and copyright information please see the LEGAL file in the code repository */

package lvsp

import (
	"libgo/protocol"

	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID            //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
// LawVoting_Status_ = Status(Quiddity_Status_FreeFlag << iota)
)
