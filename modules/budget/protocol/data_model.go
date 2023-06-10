/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	urp "org/modules/user-request/protocol"
)

type BudgetUUID = protocol.UUID

// TODO::: move all budget to the base domain

// Budget indicate the domain record data fields.
type Budget interface {
	BudgetID() BudgetUUID //
	OrgID() OrgUUID
	Type() Budget_Type
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProjectBudget_StorageServices interface {
	Save(dm Budget) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(budgetID BudgetUUID, orgID OrgUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(budgetID BudgetUUID, orgID OrgUUID, vo protocol.VersionOffset) (dm Budget, nv protocol.NumberOfVersion, err protocol.Error)
}

type Budget_Type uint16

// https://www.linkedin.com/pulse/5-budgeting-methods-everyone-should-know-about-advantages-ehab-sobhy/
const (
	Budget_Type_Unset Budget_Type = iota
	Budget_Type_Zero_based
	Budget_Type_Incremental
	Budget_Type_Activity_Based
	Budget_Type_Value_Proposition
	Budget_Type_Flexible
)
