/* For license and copyright information please see the LEGAL file in the code repository */

package nwp

import (
	"memar/protocol"
	"memar/time/earth"
	"memar/time/utc"

	aap "org/modules/app-audit/protocol"
	anp "org/modules/app-node/protocol"
	np "org/modules/notification/protocol"
)

type DataModel interface {
	NotificationID() np.NotificationUUID
	NodeID() anp.NodeUUID
	Week() utc.Weekdays
	DayHours() earth.DayHours // what hours in above days notification serve

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
