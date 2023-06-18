/* For license and copyright information please see the LEGAL file in the code repository */

package vpp

import (
	"libgo/protocol"

	pp "org/modules/pos/protocol"
	urp "org/modules/user-request/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID      //
	PosID() pp.PosUUID              //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
