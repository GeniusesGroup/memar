/* For license and copyright information please see the LEGAL file in the code repository */

package vvp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID      //
	Each() uint8                    // Each time use
	Percentage() protocol.PerMyriad // Max discount percentage per use
	Price() protocol.MoneyAmount    // Max discount price per use
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
