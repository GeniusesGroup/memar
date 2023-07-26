/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"

	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

// DataModel is UserNotificationTimeline domain record data fields.
type DataModel interface {
	UserID() up.UserUUID
	GroupID() gp.GroupUUID // generate for group & comment domain

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
