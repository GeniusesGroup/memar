/* For license and copyright information please see the LEGAL file in the code repository */

package udp

import (
	"libgo/protocol"

	qsp "org/modules/quiddity-status/protocol"
	rp "org/modules/role/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
	
)

// DataModel means transfer power to someone. power is role access in softwares.

// DataModel indicate the domain record data fields.
type DataModel interface {
	GivenUserID() up.UserUUID       //
	GottenUserID() up.UserUUID      //
	RoleID() rp.RoleUUID            //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
// Status_ = Status(Quiddity_Status_FreeFlag << iota)
)

// Service: delegate user can delegate its role to other. blocked this service by default.
