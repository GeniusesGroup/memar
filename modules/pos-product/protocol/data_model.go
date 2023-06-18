/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	"libgo/protocol"

	pp "org/modules/pos/protocol"
	prp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// Save shortcut to regular products to easily add to invoice
type DataModel interface {
	PosID() pp.PosUUID              //
	ProductID() []prp.ProductUUID   //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
