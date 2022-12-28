/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// InvoiceItemReserveTime indicate the domain record data fields.
type InvoiceItemReserveTime interface {
	InvoiceID() [16]byte        // invoice domain
	ProductID() [16]byte        // product domain
	Start() protocol.Time       //
	End() protocol.Time         //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type InvoiceItemReserveTime_StorageServices interface {
	Save(itr InvoiceItemReserveTime) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID [16]byte, vo protocol.VersionOffset) (itr InvoiceItemReserveTime, nv protocol.NumberOfVersion, err protocol.Error)
}
