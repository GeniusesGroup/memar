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
	Save(dm InvoiceItemSeat) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID InvoiceUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID InvoiceUUID, vo protocol.VersionOffset) (dm InvoiceItemSeat, nv protocol.NumberOfVersion, err protocol.Error)
}

type InvoiceItemSeat_Status Quiddity_Status

const (
	InvoiceItemSeat_Status_Voided = InvoiceItemSeat_Status(Quiddity_Status_FreeFlag << iota)
)

// service: reserve seat

// FIND_InvoiceIDs_BY_ProductIDAndSeatID(productID ProductUUID, seatID uint64, offset, limit uint64) (invoiceIDs []InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
// FIND_InvoiceIDs_BY_SeatID_AND_Status(seatID uint64, status InvoiceItemSeat_Status, offset, limit uint64) (invoiceIDs []InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
// FILTER_InvoiceIDs_BY_Status(status InvoiceItemSeat_Status, offset, limit uint64) (invoiceIDs []InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
