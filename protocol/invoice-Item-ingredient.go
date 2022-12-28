/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
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
	RequestID() UserRequestUUID               // user-request domain
}

type InvoiceItemIngredient_Status uint8

const (
	InvoiceItemIngredient_Status_Unset    InvoiceItemIngredient_Status = 0
	InvoiceItemIngredient_Status_DoNotAdd InvoiceItemIngredient_Status = (1 << iota)
	InvoiceItemIngredient_Status_SoftDelete
	InvoiceItemIngredient_Status_Extra
)
