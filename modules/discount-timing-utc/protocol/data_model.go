/* For license and copyright information please see the LEGAL file in the code repository */

package dtup

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
	dp "org/modules/discount/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID    //
	Weekdays() utc.Weekdays         // what days in weekday in utc time week allow to use this discount
	DayHours() earth.DayHours       // what hours in day in utc time week allow to use this discount
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}


