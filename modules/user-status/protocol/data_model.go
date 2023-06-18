/* For license and copyright information please see the LEGAL file in the code repository */

package usp

import (
	"libgo/protocol"

	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID            // Generated unique ID for the user
	OrgID() up.UserUUID             //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
// Status_ = Status(Quiddity_Status_FreeFlag << iota)
)
