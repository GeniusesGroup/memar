/* For license and copyright information please see the LEGAL file in the code repository */

package ndndtp

import (
	"memar/protocol"
	"memar/time/earth"
	"memar/time/utc"

	arp "org/modules/app-request/protocol"
	np "org/modules/notification/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID
	NotificationID() np.NotificationUUID
	Week() utc.Weekdays
	DayHours() earth.DayHours // what hours in above days notification not serve

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
