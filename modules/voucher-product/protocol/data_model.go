/* For license and copyright information please see the LEGAL file in the code repository */

package vpp

import (
	aap "org/modules/app-audit/protocol"
	pp "org/modules/product/protocol"
	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel restrict use voucher on specific product
type DataModel interface {
	vp.VoucherID
	Each() vp.Each
	ProductID() []pp.ProductUUID

	aap.AuditRequest
	sp.SaveTime
}
