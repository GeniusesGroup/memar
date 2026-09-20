/* For license and copyright information please see the LEGAL file in the code repository */

package nhp

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"
	notification_p "org/modules/computer/notification/protocol"
)

type DataModel interface {
	notification_p.Field_NotificationID
	SignalPreference() SignalPreference

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
