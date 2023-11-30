/* For license and copyright information please see the LEGAL file in the code repository */

package vpp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	pp "org/modules/product/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel restrict use voucher on specific product
type DataModel interface {
	VoucherID() vp.VoucherUUID
	Each() vp.Each
	ProductID() []pp.ProductUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
