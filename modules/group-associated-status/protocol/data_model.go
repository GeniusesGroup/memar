/* For license and copyright information please see the LEGAL file in the code repository */

package gasp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields
type DataModel interface {
	GroupID() gp.GroupUUID          //
	UserID() up.UserUUID            //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
	Status_Joined = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_Blocked
	Status_Muted

	Status_WaitToAcceptByAdmins
	Status_WaitToAcceptByUser
)
