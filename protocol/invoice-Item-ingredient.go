/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// InvoiceItem indicate the domain record data fields.
type InvoiceItemIngredient interface {
	InvoiceID() InvoiceUUID                   //
	ProductID() ProductUUID                   //
	IngredientID() ProductUUID                //
	IngredientUnit() QuiddityRelationTypeUUID //
	Quantity() uint64                         // decimal >> 1.5 >> 1.2 >> 10 >> 0
	Status() InvoiceItemIngredient_Status     //
	Time() protocol.Time                      // save time
	RequestID() urp.UserRequestUUID           //
}

type InvoiceItemIngredient_StorageServices interface {
	Save(dm InvoiceItemIngredient) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID InvoiceUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID InvoiceUUID, vo protocol.VersionOffset) (dm InvoiceItemIngredient, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_InvoiceIDs_BY_IngredientID(IngredientID ProductUUID, offset, limit uint64) (invoiceIDs []InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type InvoiceItemIngredient_Status uint8

const (
	InvoiceItemIngredient_Status_Unset    InvoiceItemIngredient_Status = 0
	InvoiceItemIngredient_Status_DoNotAdd InvoiceItemIngredient_Status = (1 << iota)
	InvoiceItemIngredient_Status_SoftDelete
	InvoiceItemIngredient_Status_Extra
)

// LIST_ProductIDs_BY_InvoiceID(invoiceID InvoiceUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
// LIST_IngredientIDs_BY_InvoiceID_AND_ProductID(invoiceID InvoiceUUID, productID ProductUUID, offset, limit uint64) (IngredientIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
