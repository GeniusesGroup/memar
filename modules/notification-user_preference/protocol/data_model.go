/* For license and copyright information please see the LEGAL file in the code repository */

package nupp

import (
	"libgo/protocol"

	np "org/modules/notification/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID                 //
	NotificationID() np.NotificationUUID //
	SignalPreference() SignalPreference  //
	SaveTime() protocol.Time             //
	RequestID() urp.UserRequestUUID      //
}

type SignalPreference uint8

const (
	SignalPreference_Unset SignalPreference = 0
	SignalPreference_App   SignalPreference = (1 << iota)
	SignalPreference_WebApp
	SignalPreference_Email
	SignalPreference_SMS
)
