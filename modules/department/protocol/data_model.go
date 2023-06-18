/* For license and copyright information please see the LEGAL file in the code repository */

package dp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)



// DataModel indicate the domain record data fields.
// It can use to show organizational chart. Also staffs can join to the related group.
type DataModel interface {
	DepartmentID() DepartmentUUID   //
	ParentID() DepartmentUUID       // DepartmentID, Exist if it isn't top of the organization.
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

