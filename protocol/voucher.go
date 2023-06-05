/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type VoucherUUID = protocol.UUID

// Voucher indicate the domain record data fields.
// Voucher or gift voucher is a bond of the redeemable transaction type which is worth a certain monetary value and
// which may be spent only for specific reasons or on specific products
type Voucher interface {
	VoucherID() VoucherUUID //
	MaxEachUse() uint8
	Type() Voucher_Type             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type Voucher_StorageServices interface {
	Save(dm Voucher) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, vo protocol.VersionOffset) (dm Voucher, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_VoucherIDs_BY_Type(t Voucher_Type, offset, limit uint64) (voucherIDs []VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type Voucher_Type uint32

const (
	Voucher_Type_Unset  Voucher_Type = 0
	Voucher_Type_Estate Voucher_Type = (1 << iota)
	Voucher_Type_Campaign
	Voucher_Type_Category
	Voucher_Type_Duration
	Voucher_Type_Group
	Voucher_Type_Invoice
	Voucher_Type_POS
	Voucher_Type_Product
	Voucher_Type_SourceInvoice
	Voucher_Type_Usage    // limit to usage number
	Voucher_Type_UserType // limit to user type
	Voucher_Type_User     // limit to specific users
)
