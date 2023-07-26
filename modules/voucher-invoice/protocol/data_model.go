/* For license and copyright information please see the LEGAL file in the code repository */

package vip

import (
	"memar/protocol"

	vp "org/modules/voucher/protocol"
)

// TODO::: Currency??

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID
	Each() vp.Each
	MinPrice() protocol.MoneyAmount // Minimum invoice price
	MinAmount() uint64              // Minimum invoice product numbers

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
