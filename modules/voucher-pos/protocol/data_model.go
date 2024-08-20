/* For license and copyright information please see the LEGAL file in the code repository */

package vpp

import (
	aap "org/modules/app-audit/protocol"
	pp "org/modules/pos/protocol"
	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	vp.VoucherID
	PosID() pp.PosUUID

	aap.AuditRequest
	sp.SaveTime
}
