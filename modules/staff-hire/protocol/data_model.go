/* For license and copyright information please see the LEGAL file in the code repository */

package shp

import (
	"libgo/protocol"

	rp "org/modules/role/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID            //
	RoleID() rp.RoleUUID            //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
