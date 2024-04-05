/* For license and copyright information please see the LEGAL file in the code repository */

package vutp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
// Use to restrict the voucher usage by specific user type.
type DataModel interface {
	VoucherID() vp.VoucherUUID
	UserType() protocol.UserType

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
