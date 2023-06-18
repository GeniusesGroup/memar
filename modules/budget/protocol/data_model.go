/* For license and copyright information please see the LEGAL file in the code repository */

/* For license and copyright information please see the LEGAL file in the code repository */

package bp

import (
	org "org/modules/org/protocol"
	urp "org/modules/user-request/protocol"

	"libgo/protocol"
)

// TODO::: move all budget to the base domain

// Budget indicate the domain record data fields.
type DataModel interface {
	BudgetID() BudgetUUID           //
	OrgID() org.OrgUUID             //
	Type() Type                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint16

// https://www.linkedin.com/pulse/5-budgeting-methods-everyone-should-know-about-advantages-ehab-sobhy/
const (
	Type_Unset Type = iota
	Type_Zero_based
	Type_Incremental
	Type_Activity_Based
	Type_Value_Proposition
	Type_Flexible
)
