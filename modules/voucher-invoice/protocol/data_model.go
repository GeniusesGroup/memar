/* For license and copyright information please see the LEGAL file in the code repository */

package vip

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID      //
	Each() uint8                    // Each time use
	MinPrice() int64                // Minimum invoice price
	MinAmount() uint64              // Minimum invoice product numbers
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
