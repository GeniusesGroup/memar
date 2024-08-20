/* For license and copyright information please see the LEGAL file in the code repository */

package vup

import (
	aap "org/modules/app-audit/protocol"
	sp "org/modules/storage/protocol"
	up "org/modules/user/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
// Use to restrict the voucher usage by specific users.
type DataModel interface {
	vp.VoucherID
	UserID() up.UserUUID

	aap.AuditRequest
	sp.SaveTime
}
