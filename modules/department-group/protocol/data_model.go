/* For license and copyright information please see the LEGAL file in the code repository */

package dgp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	dp "org/modules/department/protocol"
	gp "org/modules/group/protocol"
)

type DataModel interface {
	DepartmentID() dp.DepartmentUUID // quiddity domain. use to get and show locale title.
	GroupID() gp.GroupUUID
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}


