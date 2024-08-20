/* For license and copyright information please see the LEGAL file in the code repository */

package vup

import (
	aap "org/modules/app-audit/protocol"
	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	vp.VoucherID
	MaximumInvoice() uint64

	aap.AuditRequest
	sp.SaveTime
}
