/* For license and copyright information please see the LEGAL file in the code repository */

package drop

import (
	"libgo/protocol"

	dp "org/modules/department/protocol"
	org "org/modules/org/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	OwnerID() org.OrgUUID            //
	DepartmentID() dp.DepartmentUUID //
	SaveTime() protocol.Time         //
	RequestID() urp.UserRequestUUID  //
}

