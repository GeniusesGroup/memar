/* For license and copyright information please see the LEGAL file in the code repository */

package iip

import (
	"libgo/protocol"

	ip "org/modules/invoice/protocol"
	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// each InvoiceItem is immutable record and so use version mechanism to chain InvoiceItem in InvoiceID group.
// Ship service can add as an item to invoice
// Each item must check for reserve validity and make action in end of validity
type DataModel interface {
	InvoiceID() ip.InvoiceUUID      //
	ProductID() pp.ProductUUID      //
	Quantity() uint64               // decimal >> 1.5 >> 1.2 >> 10 >> 0
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
