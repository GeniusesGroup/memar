/* For license and copyright information please see the LEGAL file in the code repository */

package cugsp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID                 //
	GroupID() gp.GroupUUID               //
	ReadUntil() protocol.NumberOfVersion //
	SaveTime() protocol.Time             //
	RequestID() urp.UserRequestUUID      //
}

