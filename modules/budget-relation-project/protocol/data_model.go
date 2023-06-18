/* For license and copyright information please see the LEGAL file in the code repository */

package brpp

import (
	"libgo/protocol"
	bp "org/modules/budget/protocol"
	pp "org/modules/project/protocol"
	tp "org/modules/task/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID        //
	ProjectID() pp.ProjectUUID      //
	TaskID() tp.TaskUUID            //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
