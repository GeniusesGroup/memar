/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	urp "org/modules/user-request/protocol"
)

// BudgetContractRelation indicate the domain record data fields.
type BudgetContractRelation interface {
	BudgetID() BudgetUUID              //
	ContractID() ContractUUID          //
	Status() BudgetContract_Status     //
	Time() protocol.Time               // save time
	RequestID() urp.UserRequestUUID    //
}

type BudgetContractRelation_StorageServices interface {
	Save(dm BudgetContractRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(budgetID BudgetUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(budgetID BudgetUUID, vo protocol.VersionOffset) (dm BudgetContractRelation, nv protocol.NumberOfVersion, err protocol.Error)
}

type BudgetContract_Status Quiddity_Status

