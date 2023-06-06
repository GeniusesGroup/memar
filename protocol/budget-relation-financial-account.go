/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	urp "org/modules/user-request/protocol"
)

// BudgetFinancialAccount indicate the domain record data fields.
type BudgetFinancialAccount interface {
	BudgetID() BudgetUUID                  //
	AccountID() FinancialAccountUUID       //
	Type() BudgetFinancialAccount_Type     //
	Status() BudgetFinancialAccount_Status //
	Time() protocol.Time                   // save time
	RequestID() urp.UserRequestUUID        //
}

type BudgetFinancialAccount_StorageServices interface {
	Save(dm BudgetFinancialAccount) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID ProjectUUID, accountID FinancialAccountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID ProjectUUID, accountID FinancialAccountUUID, vo protocol.VersionOffset) (dm BudgetFinancialAccount, nv protocol.NumberOfVersion, err protocol.Error)
}

type BudgetFinancialAccount_Type uint8

const (
	BudgetFinancialAccount_Type_Unset BudgetFinancialAccount_Type = iota
	BudgetFinancialAccount_Type_withdrawal
	BudgetFinancialAccount_Type_Deposit
	BudgetFinancialAccount_Type_Suggester
)

type BudgetFinancialAccount_Status Quiddity_Status
