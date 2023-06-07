/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// InvoicePOS indicate the domain record data fields.
type InvoicePOS interface {
	InvoiceID() InvoiceUUID //
	// InvoiceNumber() uint16      // TODO::: do we need auto increment number? Why not QR code?
	PosID() PosUUID                 //
	StaffID() StaffUUID             // OrdererID that is creator of the invoice e.g. restaurant, drug prescription, sales agent,
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type InvoicePOS_StorageServices interface {
	Save(dm InvoicePOS) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(invoiceID InvoiceUUID) (dm InvoicePOS, err protocol.Error)

	FIND_InvoiceIDs_BY_PosID(posID PosUUID, offset, limit uint64) (invoiceIDs []InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FIND_InvoiceIDs_BY_StaffID(staffID StaffUUID, offset, limit uint64) (invoiceIDs []InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
