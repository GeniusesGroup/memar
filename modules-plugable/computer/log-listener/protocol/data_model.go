/* For license and copyright information please see the LEGAL file in the code repository */

package nap

import (
	log_p "memar/process/log/protocol"
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	instance_p "org/modules/computer/instance_of/protocol"
	bm_p "org/modules/computer/module/protocol"
	user_p "org/modules/identity/user/protocol"
)

type DataModel interface {
	user_p.Field_UserUUID
	instance_p.Field_InstanceUUID
	NotificationChannel()
	bm_p.Field_ModuleUUID
	LogLevel() log_p.Level
	// TODO::: other condition

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
