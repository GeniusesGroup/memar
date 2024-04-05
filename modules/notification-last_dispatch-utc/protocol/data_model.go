/* For license and copyright information please see the LEGAL file in the code repository */

package nldp

import (
	"memar/protocol"
	"memar/time/utc"

	aap "org/modules/app-audit/protocol"
	np "org/modules/notification/protocol"
)

type DataModel interface {
	NotificationID() np.NotificationUUID
	Last() utc.Time

	aap.AuditRequest
	protocol.Storage_SaveTime
}
