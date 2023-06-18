/* For license and copyright information please see the LEGAL file in the code repository */

package garp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	rp "org/modules/role/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	GroupID() gp.GroupUUID          //
	UserID() up.UserUUID            //
	RoleID() rp.RoleUUID            //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
