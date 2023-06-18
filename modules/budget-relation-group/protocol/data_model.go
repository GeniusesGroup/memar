/* For license and copyright information please see the LEGAL file in the code repository */

package brgp

import (
	"libgo/protocol"
	bp "org/modules/budget/protocol"
	gp "org/modules/group/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID //
	GroupID() gp.GroupUUID   //

	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
