/* For license and copyright information please see the LEGAL file in the code repository */

package vpp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	pp "org/modules/product/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel restrict use voucher on specific product
type DataModel interface {
	VoucherID() vp.VoucherUUID
	Each() vp.Each
	ProductID() []pp.ProductUUID

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
