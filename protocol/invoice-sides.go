/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// InvoiceSides indicate the domain record data fields.
type InvoiceSides interface {
	InvoiceID() [16]byte         // invoice domain
	UserID() protocol.UserID     // user domain
	Type() InvoiceSides_Type     //
	Status() InvoiceSides_Status //
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

type InvoiceSides_StorageServices interface {
	Save(is InvoiceSides) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID [16]byte, vo protocol.VersionOffset) (is InvoiceSides, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUser(userID [16]byte, typ InvoiceSides_Type, offset, limit uint64) (invoiceIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type InvoiceSides_Type uint8

const (
	InvoiceSides_Type_Seller InvoiceSides_Type = iota
	InvoiceSides_Type_Customer
	InvoiceSides_Type_Agent
	InvoiceSides_Type_Franchise
)

type InvoiceSides_Status = Quiddity_Status

const (
// InvoiceSides_Status_ = InvoiceSides_Status(Quiddity_Status_FreeFlag << iota)
)
