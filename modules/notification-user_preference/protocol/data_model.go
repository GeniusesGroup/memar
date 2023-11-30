/* For license and copyright information please see the LEGAL file in the code repository */

package nupp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	np "org/modules/notification/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID
	NotificationID() np.NotificationUUID
	SignalPreference() SignalPreference

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
