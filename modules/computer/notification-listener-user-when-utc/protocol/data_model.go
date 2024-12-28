/* For license and copyright information please see the LEGAL file in the code repository */

package nluwp

import (
	"memar/protocol"
	"memar/time/earth"
	"memar/time/utc"

	aap "org/modules/app-audit/protocol"
	np "org/modules/notification/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	NotificationID() np.NotificationUUID
	UserID() up.UserUUID
	Week() utc.Weekdays
	DayHours() earth.DayHours // what hours in above days notification serve

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
