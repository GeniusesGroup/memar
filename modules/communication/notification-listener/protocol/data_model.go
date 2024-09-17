/* For license and copyright information please see the LEGAL file in the code repository */

package nlp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	anp "org/modules/app-node/protocol"
	np "org/modules/notification/protocol"
)

type DataModel interface {
	NotificationID() np.NotificationUUID
	NodeID() anp.NodeUUID
	Status() Status

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
