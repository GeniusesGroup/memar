/* For license and copyright information please see the LEGAL file in the code repository */

package dgp

import (
	"libgo/protocol"

	dp "org/modules/discount/protocol"
	gp "org/modules/group/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID    //
	GroupID() gp.GroupUUID          //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
