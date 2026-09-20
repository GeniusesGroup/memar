/* For license and copyright information please see the LEGAL file in the code repository */

package np

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type NotificationTemplate interface {
	NotificationID() NotificationUUID //
	UserID() up.UserUUID              //
	SaveTime() protocol.Time              // save time
	RequestID() urp.UserRequestUUID   //
}
