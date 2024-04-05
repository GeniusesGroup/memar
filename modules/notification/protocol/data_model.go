/* For license and copyright information please see the LEGAL file in the code repository */

package np

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	anp "org/modules/app-node/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	NotificationID() NotificationUUID
	UserID() up.UserUUID
	NodeID() anp.NodeUUID
	DeliveryType() DeliveryType

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
