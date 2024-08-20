/* For license and copyright information please see the LEGAL file in the code repository */

package vp

import (
	aap "org/modules/app-audit/protocol"
	sp "org/modules/storage/protocol"
)

// DataModel indicate the domain record data fields.
// Voucher or gift voucher is a bond of the redeemable transaction type which is worth a certain monetary value and
// which may be spent only for specific reasons or on specific products
type DataModel interface {
	VoucherID
	MaxEachUse() MaxEachUse
	Type() Type

	aap.AuditRequest
	sp.SaveTime
}
