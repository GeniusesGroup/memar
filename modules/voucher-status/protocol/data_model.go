/* For license and copyright information please see the LEGAL file in the code repository */

package vsp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID
	Status() Status

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
