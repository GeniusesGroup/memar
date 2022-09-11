/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// InvoicePOS indicate the domain record data fields.
type InvoicePOS interface {
	InvoiceID() [16]byte        // invoice domain
	PosID() [16]byte            // pos domain
	StaffID() [16]byte          // staff domain. or OrdererID that is creator of the invoice e.g. restaurant, drug prescription, sales agent,
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type InvoicePOS_StorageServices interface {
	Save(ip InvoicePOS) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(invoiceID [16]byte) (ip InvoicePOS, err protocol.Error)

	FindByPos(posID [16]byte, offset, limit uint64) (invoiceIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	FindByStaff(staffID [16]byte, offset, limit uint64) (invoiceIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
