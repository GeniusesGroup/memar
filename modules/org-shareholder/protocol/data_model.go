/* For license and copyright information please see the LEGAL file in the code repository */

package osp

import (
	"libgo/protocol"

	org "org/modules/org/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	OrgID() org.OrgUUID
	UserID() up.UserUUID            //
	Quantity() protocol.PerTrillion //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

