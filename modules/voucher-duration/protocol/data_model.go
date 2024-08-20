/* For license and copyright information please see the LEGAL file in the code repository */

package vdp

import (
	"memar/time/duration"

	aap "org/modules/app-audit/protocol"
	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	vp.VoucherID
	Each() vp.Each
	Epoch() Epoch
	Duration() duration.Second // from Epoch()

	aap.AuditRequest
	sp.SaveTime
}
