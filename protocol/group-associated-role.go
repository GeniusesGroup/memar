/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// GroupAssociatedRole indicate the domain record data fields.
type GroupAssociatedRole interface {
	GroupID() GroupUUID             //
	UserID() up.UserUUID            //
	RoleID() RoleUUID               //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
