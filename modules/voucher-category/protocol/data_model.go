/* For license and copyright information please see the LEGAL file in the code repository */

package vcp

import (
	"libgo/protocol"

	cp "org/modules/category/protocol"
	urp "org/modules/user-request/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
// Use to restrict the voucher on specific category.
type DataModel interface {
	VoucherID() vp.VoucherUUID      //
	Each() uint8                    // Each time use
	CategoryID() []cp.CategoryUUID  //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}


