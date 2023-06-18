/* For license and copyright information please see the LEGAL file in the code repository */

package rsp

import (
	"libgo/protocol"

	rp "org/modules/role/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	RoleID() rp.RoleUUID            //
	Minimum() int                   // Minimum number of employees for this job position
	Expected() int                  // Expected number of employees for this job position
	Maximum() int                   // Maximum number of employees for this job position
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
