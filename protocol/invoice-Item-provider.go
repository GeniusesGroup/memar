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
	Save(f InvoiceItemProvider) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID InvoiceUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID InvoiceUUID, vo protocol.VersionOffset) (f InvoiceItemProvider, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_InvoiceIDs_BY_StaffID(staffID StaffUUID, offset, limit uint64) (invoiceIDs []InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

//	LIST_StaffIDs_BY_InvoiceID_And_ProductID(invoiceID InvoiceUUID, productID ProductUUID, offset, limit uint64) (staffIDs []StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)
// FIND_InvoiceIDs_BY_ProductID_AND_StaffID(productID ProductUUID, staffID StaffUUID, offset, limit uint64) (invoiceIDs []InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
