/* For license and copyright information please see the LEGAL file in the code repository */

package vdp

import (
	"memar/protocol"

	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID
	Each() vp.Each
	Epoch() Epoch
	Duration() protocol.Duration // from Epoch()

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
