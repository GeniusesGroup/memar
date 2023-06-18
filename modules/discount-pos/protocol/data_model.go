/* For license and copyright information please see the LEGAL file in the code repository */

package dpp

import (
	"libgo/protocol"

	dp "org/modules/discount/protocol"
	pp "org/modules/pos/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID    //
	PosID() pp.PosUUID              //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

