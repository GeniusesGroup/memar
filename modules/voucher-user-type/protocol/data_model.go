/* For license and copyright information please see the LEGAL file in the code repository */

package vutp

import (
	"memar/protocol"

	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
// Use to restrict the voucher usage by specific user type.
type DataModel interface {
	VoucherID() vp.VoucherUUID
	UserType() protocol.UserType

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
