/* For license and copyright information please see the LEGAL file in the code repository */

package ndndtp

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	np "org/modules/notification/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID                 //
	NotificationID() np.NotificationUUID //
	Week() utc.Weekdays                  //
	DayHours() earth.DayHours            // what hours in above days notification not serve
	SaveTime() protocol.Time             //
	RequestID() urp.UserRequestUUID      //
}
