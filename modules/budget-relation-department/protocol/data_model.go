/* For license and copyright information please see the LEGAL file in the code repository */

package brdp

import (
	"libgo/protocol"
	bp "org/modules/budget/protocol"
	dp "org/modules/department/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID         //
	DepartmentID() dp.DepartmentUUID //
	SaveTime() protocol.Time         //
	RequestID() urp.UserRequestUUID  //
}
