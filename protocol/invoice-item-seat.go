/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// InvoiceItemSeat indicate the domain record data fields.
// It can also use to order buyers e.g. patient in doctor clinic.
type InvoiceItemSeat interface {
	InvoiceID() InvoiceUUID         //
	ProductID() ProductUUID         //
	SeatID() uint64                 // seat number
	Status() InvoiceItemSeat_Status //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type InvoiceItemSeat_StorageServices interface {
	Save(iis InvoiceItemSeat) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID [16]byte, vo protocol.VersionOffset) (iis InvoiceItemSeat, nv protocol.NumberOfVersion, err protocol.Error)
}

type InvoiceItemSeat_Status Quiddity_Status

const (
	InvoiceItemSeat_Status_Voided = InvoiceItemSeat_Status(Quiddity_Status_FreeFlag << iota)
)

// service: reserve seat
