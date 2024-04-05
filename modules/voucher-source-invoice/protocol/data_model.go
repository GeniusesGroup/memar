/* For license and copyright information please see the LEGAL file in the code repository */

package vsip

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	ip "org/modules/invoice/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID
	InvoiceID() ip.InvoiceUUID
	InvoiceType() Type

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
