/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	urp "org/modules/user-request/protocol"
)

// BudgetBudgetRelation indicate the domain record data fields.
type BudgetBudgetRelation interface {
	BudgetID() BudgetUUID      //
	OtherBudgetID() BudgetUUID //
	Type() BudgetBudgetRelation_Type
	Status() BudgetBudget_Status
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type BudgetBudgetRelation_StorageServices interface {
	Save(dm BudgetBudgetRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(budgetID BudgetUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(budgetID BudgetUUID, vo protocol.VersionOffset) (dm BudgetBudgetRelation, nv protocol.NumberOfVersion, err protocol.Error)
}

type BudgetBudget_Status Quiddity_Status

type BudgetBudgetRelation_Type uint8

const (
	BudgetBudgetRelation_Type_Unset BudgetBudgetRelation_Type = iota
	BudgetBudgetRelation_Type_Blocking
	BudgetBudgetRelation_Type_Complement
	BudgetBudgetRelation_Type_Continuous
)
