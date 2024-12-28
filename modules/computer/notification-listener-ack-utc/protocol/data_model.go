/* For license and copyright information please see the LEGAL file in the code repository */

package nlap

import (
	"memar/protocol"
	"memar/time/utc"

	aap "org/modules/app-audit/protocol"
	anp "org/modules/app-node/protocol"
	np "org/modules/notification/protocol"
)

type DataModel interface {
	NotificationID() np.NotificationUUID
	NodeID() anp.NodeUUID
	Last() utc.Time

	aap.AuditRequest
	protocol.Storage_SaveTime
}
