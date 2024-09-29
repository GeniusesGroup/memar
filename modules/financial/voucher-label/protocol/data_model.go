/* For license and copyright information please see the LEGAL file in the code repository */

package vcp

import (
	aap "org/modules/app-audit/protocol"
	cp "org/modules/category/protocol"
	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
// Use to restrict the voucher on specific category.
type DataModel interface {
	vp.VoucherID
	Each() vp.Each
	CategoryID() []cp.CategoryUUID

	aap.AuditRequest
	sp.SaveTime
}
