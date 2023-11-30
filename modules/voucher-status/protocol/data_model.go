/* For license and copyright information please see the LEGAL file in the code repository */

package vsp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
