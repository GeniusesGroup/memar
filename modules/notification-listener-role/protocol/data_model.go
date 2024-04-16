/* For license and copyright information please see the LEGAL file in the code repository */

package nlrp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	np "org/modules/notification/protocol"
	rp "org/modules/role/protocol"
)

type DataModel interface {
	NotificationID() np.NotificationUUID
	RoleID() rp.RoleUUID
	Status() Status

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
