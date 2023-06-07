/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// InvoiceSides indicate the domain record data fields.
type InvoiceSides interface {
	InvoiceID() InvoiceUUID         //
	UserID() up.UserUUID            //
	Type() InvoiceSides_Type        //
	Status() InvoiceSides_Status    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type InvoiceSides_StorageServices interface {
	Save(dm InvoiceSides) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID InvoiceUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID InvoiceUUID, vo protocol.VersionOffset) (dm InvoiceSides, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_InvoiceIDs_BY_UserID_AND_Type(userID up.UserUUID, t InvoiceSides_Type, offset, limit uint64) (invoiceIDs []InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type InvoiceSides_Type uint8

const (
	InvoiceSides_Type_Seller InvoiceSides_Type = iota
	InvoiceSides_Type_Customer
	InvoiceSides_Type_Agent
	InvoiceSides_Type_Franchise
)

type InvoiceSides_Status Quiddity_Status

const (
// InvoiceSides_Status_ = InvoiceSides_Status(Quiddity_Status_FreeFlag << iota)
)
