/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// InvoiceItemProvider indicate the domain record data fields.
type InvoiceItemProvider interface {
	InvoiceID() InvoiceUUID         //
	ProductID() ProductUUID         //
	StaffID() StaffUUID             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type InvoiceItemProvider_StorageServices interface {
	Save(iip InvoiceItemProvider) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID [16]byte, vo protocol.VersionOffset) (iip InvoiceItemProvider, nv protocol.NumberOfVersion, err protocol.Error)

	FindByStaff(staffID [16]byte, offset, limit uint64) (invoiceIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
