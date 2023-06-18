/* For license and copyright information please see the LEGAL file in the code repository */

package ptup

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	ProductID() pp.ProductUUID      //
	Day() utc.DayElapsed            //
	DayHours() earth.DayHours       // what hours in a day this service active to provide services
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
