/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	urp "org/modules/user-request/protocol"
)

// BudgetInvoiceRelation indicate the domain record data fields.
type BudgetInvoiceRelation interface {
	BudgetID() BudgetUUID             //
	InvoiceID() InvoiceUUID           //
	Type() BudgetInvoiceRelation_Type //
	Status() BudgetInvoice_Status     //
	Time() protocol.Time              // save time
	RequestID() urp.UserRequestUUID   //
}

type BudgetInvoiceRelation_StorageServices interface {
	Save(dm BudgetInvoiceRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(budgetID BudgetUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(budgetID BudgetUUID, vo protocol.VersionOffset) (dm BudgetInvoiceRelation, nv protocol.NumberOfVersion, err protocol.Error)
}

type BudgetInvoice_Status Quiddity_Status

type BudgetInvoiceRelation_Type uint8

const (
	BudgetInvoiceRelation_Type_Unset BudgetInvoiceRelation_Type = iota
	BudgetInvoiceRelation_Type_Supporter
	BudgetInvoiceRelation_Type_Sponsor
)
