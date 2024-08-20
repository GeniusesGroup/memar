/* For license and copyright information please see the LEGAL file in the code repository */

package vsip

import (
	aap "org/modules/app-audit/protocol"
	ip "org/modules/invoice/protocol"
	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	vp.VoucherID
	InvoiceID() ip.InvoiceUUID
	InvoiceType() Type

	aap.AuditRequest
	sp.SaveTime
}
