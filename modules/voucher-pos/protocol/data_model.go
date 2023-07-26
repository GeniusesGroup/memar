/* For license and copyright information please see the LEGAL file in the code repository */

package vpp

import (
	"memar/protocol"

	pp "org/modules/pos/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID
	PosID() pp.PosUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
