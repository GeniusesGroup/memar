/* For license and copyright information please see the LEGAL file in the code repository */

package rrgp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	qsp "org/modules/quiddity-status/protocol"
	rp "org/modules/role/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	RoleID() rp.RoleUUID            //
	GroupID() gp.GroupUUID          //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status
