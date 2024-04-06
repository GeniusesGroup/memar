/* For license and copyright information please see the LEGAL file in the code repository */

package nsp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	np "org/modules/notification/protocol"
)

type DataModel interface {
	NotificationID() np.NotificationUUID
	Status() Status

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
