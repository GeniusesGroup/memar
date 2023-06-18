/* For license and copyright information please see the LEGAL file in the code repository */

package iiip

import (
	"libgo/protocol"

	ip "org/modules/invoice/protocol"
	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID      //
	ProductID() pp.ProductUUID      //
	Type() Type                     //
	ActionTime() protocol.Time      //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota

	Type_Enter
	Type_Exit
	Type_ManualEnter
	Type_ManualExit

	Type_Start
	Type_End
	Type_ManualStart
	Type_ManualEnd

	Type_Cooking
	Type_Packaging
)
