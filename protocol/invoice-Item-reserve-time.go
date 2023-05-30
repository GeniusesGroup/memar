/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// InvoiceItemReserveTime indicate the domain record data fields.
type InvoiceItemReserveTime interface {
	InvoiceID() InvoiceUUID         //
	ProductID() ProductUUID         //
	Start() protocol.Time           //
	End() protocol.Time             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type InvoiceItemReserveTime_StorageServices interface {
	Save(itr InvoiceItemReserveTime) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID [16]byte, vo protocol.VersionOffset) (itr InvoiceItemReserveTime, nv protocol.NumberOfVersion, err protocol.Error)
}
