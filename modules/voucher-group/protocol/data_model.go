/* For license and copyright information please see the LEGAL file in the code repository */

package vgp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	gp "org/modules/group/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID
	GroupID() []gp.GroupUUID

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
