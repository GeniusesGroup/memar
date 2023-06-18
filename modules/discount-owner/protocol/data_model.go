/* For license and copyright information please see the LEGAL file in the code repository */

package dop

import (
	"libgo/protocol"

	org "org/modules/org/protocol"
	urp "org/modules/user-request/protocol"
	dp "org/modules/discount/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID    //
	OrgID() org.OrgUUID             //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

