/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// InvoiceItemTime indicate the domain record data fields.
type InvoiceItemTime interface {
	InvoiceID() InvoiceUUID         //
	ProductID() ProductUUID         //
	Type() InvoiceItemTime_Type     //
	ActionTime() protocol.Time      //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type InvoiceItemTime_StorageServices interface {
	Save(dm InvoiceItemTime) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID InvoiceUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID InvoiceUUID, vo protocol.VersionOffset) (dm InvoiceItemTime, err protocol.Error)
}

type InvoiceItemTime_Type uint8

const (
	InvoiceItemTime_Type_Unset InvoiceItemTime_Type = iota

	InvoiceItemTime_Type_Enter
	InvoiceItemTime_Type_Exit
	InvoiceItemTime_Type_ManualEnter
	InvoiceItemTime_Type_ManualExit

	InvoiceItemTime_Type_Start
	InvoiceItemTime_Type_End
	InvoiceItemTime_Type_ManualStart
	InvoiceItemTime_Type_ManualEnd

	InvoiceItemTime_Type_Cooking
	InvoiceItemTime_Type_Packaging
)

// LIST_ProductIDs_BY_InvoiceID(invoiceID InvoiceUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
