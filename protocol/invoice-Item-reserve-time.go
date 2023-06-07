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
	Save(dm InvoiceItemReserveTime) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID InvoiceUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID InvoiceUUID, vo protocol.VersionOffset) (dm InvoiceItemReserveTime, nv protocol.NumberOfVersion, err protocol.Error)
}
