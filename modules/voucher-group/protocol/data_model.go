/* For license and copyright information please see the LEGAL file in the code repository */

package vgp

import (
	aap "org/modules/app-audit/protocol"
	gp "org/modules/group/protocol"
	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	vp.VoucherID
	GroupID() []gp.GroupUUID

	aap.AuditRequest
	sp.SaveTime
}
