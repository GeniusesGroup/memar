/* For license and copyright information please see the LEGAL file in the code repository */

package ip

import (
	"libgo/protocol"

	ip "org/modules/invoice/protocol"
	pp "org/modules/pos/protocol"
	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID //
	// InvoiceNumber() uint16      // TODO::: do we need auto increment number? Why not QR code?
	PosID() pp.PosUUID              //
	StaffID() sp.StaffUUID          // OrdererID that is creator of the invoice e.g. restaurant, drug prescription, sales agent,
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
