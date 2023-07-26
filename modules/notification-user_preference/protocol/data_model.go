/* For license and copyright information please see the LEGAL file in the code repository */

package nupp

import (
	"memar/protocol"

	np "org/modules/notification/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID
	NotificationID() np.NotificationUUID
	SignalPreference() SignalPreference

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
