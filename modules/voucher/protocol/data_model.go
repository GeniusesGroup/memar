/* For license and copyright information please see the LEGAL file in the code repository */

package vp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// Voucher or gift voucher is a bond of the redeemable transaction type which is worth a certain monetary value and
// which may be spent only for specific reasons or on specific products
type DataModel interface {
	VoucherID() VoucherUUID //
	MaxEachUse() uint8
	Type() Type                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint32

const (
	Type_Unset  Type = 0
	Type_Estate Type = (1 << iota)
	Type_Campaign
	Type_Category
	Type_Duration
	Type_Group
	Type_Invoice
	Type_POS
	Type_Product
	Type_SourceInvoice
	Type_Usage    // limit to usage number
	Type_UserType // limit to user type
	Type_User     // limit to specific users
)
