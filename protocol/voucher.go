/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// Voucher indicate the domain record data fields.
// Voucher or gift voucher is a bond of the redeemable transaction type which is worth a certain monetary value and
// which may be spent only for specific reasons or on specific products
type Voucher interface {
	VoucherID() [16]byte        //
	Type() Voucher_Type         //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type Voucher_StorageServices interface {
	Save(v Voucher) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID [16]byte, vo protocol.VersionOffset) (v Voucher, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(type Voucher_Type, offset, limit uint64) (voucherIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type Voucher_Type uint32

const (
	Voucher_Type_Unset Voucher_Type = 0
	Voucher_Type_Area  Voucher_Type = (1 << iota)
	Voucher_Type_Campaign
	Voucher_Type_Category
	Voucher_Type_Duration
	Voucher_Type_Group
	Voucher_Type_Invoice
	Voucher_Type_Location
	Voucher_Type_POS
	Voucher_Type_Product
	Voucher_Type_SourceInvoice
	Voucher_Type_Usage    // limit to usage number
	Voucher_Type_UserType // limit to user type
	Voucher_Type_User     // limit to specific users
)
