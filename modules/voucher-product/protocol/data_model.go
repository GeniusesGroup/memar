/* For license and copyright information please see the LEGAL file in the code repository */

package vpp

import (
	"libgo/protocol"

	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel restrict use voucher on specific product
type DataModel interface {
	VoucherID() vp.VoucherUUID      //
	Each() uint8                    // Each time use
	ProductID() []pp.ProductUUID    //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
