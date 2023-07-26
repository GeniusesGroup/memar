/* For license and copyright information please see the LEGAL file in the code repository */

package ivp

import (
	"memar/protocol"

	ip "org/modules/invoice/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
// This domain will let users redeem their vouchers and track vouchers rules.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID
	VoucherID() vp.VoucherUUID
	Discounted() protocol.MoneyAmount

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
