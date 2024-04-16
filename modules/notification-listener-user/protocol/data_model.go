/* For license and copyright information please see the LEGAL file in the code repository */

package nlup

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	np "org/modules/notification/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	NotificationID() np.NotificationUUID
	UserID() up.UserUUID
	Status() Status

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
