/* For license and copyright information please see the LEGAL file in the code repository */

package ndndtp

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	NotificationID() [16]byte       //
	Day() utc.DayElapsed            //
	DayHours() earth.DayHours       // what hours in a day notification not serve
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
