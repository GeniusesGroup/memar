/* For license and copyright information please see the LEGAL file in the code repository */

package iirtp

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
	Start() protocol.Time           //
	End() protocol.Time             //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

