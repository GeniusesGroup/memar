/* For license and copyright information please see the LEGAL file in the code repository */

package vup

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
// Use to restrict the voucher usage by specific users.
type DataModel interface {
	VoucherID() vp.VoucherUUID      //
	UserID() up.UserUUID            //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
