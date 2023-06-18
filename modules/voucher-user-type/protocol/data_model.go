/* For license and copyright information please see the LEGAL file in the code repository */

package vutp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
// Use to restrict the voucher usage by specific user type.
type DataModel interface {
	VoucherID() vp.VoucherUUID      //
	UserType() protocol.UserType    //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
