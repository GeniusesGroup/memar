/* For license and copyright information please see the LEGAL file in the code repository */

package iip

import (
	"libgo/protocol"

	ip "org/modules/invoice/protocol"
	pp "org/modules/product/protocol"
	qrtp "org/modules/quiddity-relation-type/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID                     //
	ProductID() pp.ProductUUID                     //
	IngredientID() pp.ProductUUID                  //
	IngredientUnit() qrtp.QuiddityRelationTypeUUID //
	Quantity() uint64                              // decimal >> 1.5 >> 1.2 >> 10 >> 0
	Status() Status                                //
	SaveTime() protocol.Time                       //
	RequestID() urp.UserRequestUUID                //
}

type Status uint8

const (
	Status_Unset    Status = 0
	Status_DoNotAdd Status = (1 << iota)
	Status_SoftDelete
	Status_Extra
)
