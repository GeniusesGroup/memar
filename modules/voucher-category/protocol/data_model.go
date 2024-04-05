/* For license and copyright information please see the LEGAL file in the code repository */

package vcp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	cp "org/modules/category/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
// Use to restrict the voucher on specific category.
type DataModel interface {
	VoucherID() vp.VoucherUUID
	Each() vp.Each
	CategoryID() []cp.CategoryUUID

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
