/* For license and copyright information please see the LEGAL file in the code repository */

package notification_p

import (
	group_p "org/modules/management/group/protocol"
)

type Field_NotificationID interface {
	NotificationID() NotificationUUID
}

type NotificationUUID group_p.UUID
