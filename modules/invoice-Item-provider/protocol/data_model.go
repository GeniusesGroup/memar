/* For license and copyright information please see the LEGAL file in the code repository */

package iipp

import (
	"libgo/protocol"

	ip "org/modules/invoice/protocol"
	pp "org/modules/product/protocol"
	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID      //
	ProductID() pp.ProductUUID      //
	StaffID() sp.StaffUUID          //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
