/* For license and copyright information please see the LEGAL file in the code repository */

package nsp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	np "org/modules/notification/protocol"
	qsp "org/modules/quiddity-status/protocol"
)

type DataModel interface {
	NotificationID() np.NotificationUUID
	Status() qsp.Quiddity_Status

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
