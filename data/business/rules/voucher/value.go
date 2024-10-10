/* For license and copyright information please see the LEGAL file in the code repository */

package vvp

import (
	aap "org/modules/app-audit/protocol"
	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	vp.VoucherID
	Each() vp.Each
	Proportion() Proportion
	Worth() Worth

	aap.AuditRequest
	sp.SaveTime
}
